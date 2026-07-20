import json
import os
import time
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

from aidp.discovery.debate import ScientificDebateEngine
from aidp.discovery.domain_routing import DomainDetector, DomainRouter
from aidp.discovery.hypothesis import HypothesisGenerator
from aidp.discovery.scientific_planning import AblationConfig, WetLabPlanner
from aidp.intelligence.epistemic_models import (
    EpistemicClaim,
    EpistemicEvidence,
    EpistemicReview,
    VerificationStatus,
)
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.platform.epistemic_logger import EpistemicLedger
from aidp.reasoning.confidence_calibrator import ConfidenceCalibrator, LineageEngine


class DiscoveryState(Enum):
    INIT = "INIT"
    RETRIEVAL = "RETRIEVAL"
    GAP_ANALYSIS = "GAP_ANALYSIS"
    HYPOTHESIS = "HYPOTHESIS"
    PLANNING = "PLANNING"
    FORMAL_VERIFICATION = "FORMAL_VERIFICATION"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    MEMORY_UPDATE = "MEMORY_UPDATE"
    EXECUTION = "EXECUTION"
    FINISHED = "FINISHED"
    FAILED = "FAILED"
    PAUSED = "PAUSED"


@dataclass
class DiscoverySession:
    id: str = field(default_factory=lambda: f"sess_{uuid.uuid4()}")
    question: str = ""
    historical_cutoff_date: str | None = None
    state: DiscoveryState = DiscoveryState.INIT

    knowledge_context: dict[str, Any] = field(default_factory=dict)
    contradictions: list[dict[str, Any]] = field(default_factory=list)
    gaps: list[dict[str, Any]] = field(default_factory=list)
    hypothesis: dict[str, Any] = field(default_factory=dict)
    experiment_design: dict[str, Any] = field(default_factory=dict)
    debate_record: dict[str, Any] = field(default_factory=dict)
    consensus_report: dict[str, Any] = field(default_factory=dict)

    telemetry: dict[str, Any] = field(default_factory=dict)
    trace: list[dict[str, Any]] = field(default_factory=list)
    event_payload: dict[str, Any] = field(default_factory=dict)
    paused_at_state: str | None = None

    def log_trace(self, event: str, metadata: dict[str, Any] | None = None) -> None:
        self.trace.append({"timestamp": time.time(), "event": event, "metadata": metadata or {}})

    def save_checkpoint(self, directory: str = ".checkpoints") -> None:
        if not os.path.exists(directory):
            os.makedirs(directory)
        path = os.path.join(directory, f"{self.id}.json")
        with open(path, "w") as f:
            d = asdict(self)
            d["state"] = self.state.value
            json.dump(d, f, indent=2)

    @classmethod
    def load_checkpoint(cls, filepath: str) -> "DiscoverySession":
        with open(filepath) as f:
            data = json.load(f)

        data["state"] = DiscoveryState(data["state"])
        return cls(**data)


class WorkflowNode:
    """Base class for a node in the execution DAG."""

    def __init__(self, name: str) -> None:
        self.name = name

    def execute(self, session: DiscoverySession) -> DiscoveryState:
        """
        Executes logic and returns the next state.
        Must handle its own retries or allow exceptions to bubble up to the DAG.
        Can return DiscoveryState.PAUSED to yield execution.
        """
        raise NotImplementedError

    def on_event(self, session: DiscoverySession, event_data: dict[str, Any]) -> DiscoveryState:
        """
        Called when the DAG is resumed from a PAUSED state with an external event payload.
        Should process the event and return the next state.
        """
        raise NotImplementedError("Node does not support event-driven resumption.")


# --- Node Implementations ---


class RetrievalNode(WorkflowNode):
    def __init__(self, gateway: Any) -> None:
        super().__init__("KnowledgeRetrieval")
        self.gateway = gateway

    def execute(self, session: DiscoverySession) -> DiscoveryState:
        session.log_trace("Entering Knowledge Retrieval")
        from aidp.knowledge.connectors.pubmed_connector import PubMedConnector
        from aidp.knowledge.extraction.kg_extractor import KnowledgeGraphExtractor
        from aidp.retrieval.adversarial import AdversarialQueryGenerator
        from aidp.retrieval.indexing import KnowledgeGraphIndexer
        from aidp.retrieval.ingestion import DocumentIngestor
        from aidp.retrieval.scoring import EpistemicScorer
        
        connector = PubMedConnector(max_results=3)
        ingestor = DocumentIngestor()
        indexer = KnowledgeGraphIndexer()
        adv_generator = AdversarialQueryGenerator(self.gateway)
        scorer = EpistemicScorer()
        # Robust stop word filtering for concept retention (reusing metrics logic)
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", 
            "of", "with", "by", "as", "is", "are", "was", "were", "be", "been", 
            "being", "it", "its", "that", "this", "these", "those", "what", "how", "why"
        }
        sentence = session.question
        for p in ".,;:'\"()[]{}!?":
            sentence = sentence.replace(p, " ")
        words = sentence.split()
        search_term = " ".join([w for w in words if w.lower() not in stop_words and len(w) > 2])
        
        if not search_term:
            search_term = session.question
        
        # Pass the historical cutoff date formatted as YYYY/MM/DD
        max_date = None
        if session.historical_cutoff_date:
            try:
                # If it's a datetime.date object from the benchmark, format it
                if hasattr(session.historical_cutoff_date, 'strftime'):
                    max_date = session.historical_cutoff_date.strftime("%Y/%m/%d")
                else:
                    # Attempt to parse string YYYY-MM-DD
                    max_date = session.historical_cutoff_date.replace('-', '/')
            except Exception:
                pass

        # Compartment 1C: Adversarial Retrieval
        adversarial_queries = adv_generator.generate_adversarial_queries(search_term)
        
        provenance_entries = connector.fetch_literature_provenance(search_term, max_date=max_date)
        
        adv_provenance_entries = []
        for aq in adversarial_queries:
            adv_provenance_entries.extend(connector.fetch_literature_provenance(aq, max_date=max_date))
        
        # Query Fallback Strategy: if the highly specific semantic query returns 0 results, 
        # fall back to a broader entity-only query.
        if len(provenance_entries) == 0:
            session.log_trace("Semantic query returned 0 results. Falling back to entity query.", {"failed_query": search_term})
            fallback_term = " ".join([w for w in session.question.replace('?','').split() if any(c.isupper() for c in w)])
            if fallback_term:
                provenance_entries = connector.fetch_literature_provenance(fallback_term, max_date=max_date)
                
        def process_entries(entries, is_adversarial=False):
            docs = []
            raw_docs = []
            for entry in entries:
                # Compartment 1D: Epistemic Scoring
                # Determine pseudo-year from metadata if possible, else default to current year minus 1
                year = 2026 # Default mock year
                trust_score = scorer.score_document(
                    pmid=entry.source_paper_doi,
                    title=entry.retriever_metadata.get("title", "Unknown Title"),
                    year=year
                )
                
                if trust_score.is_retracted or trust_score.score < 0.2:
                    session.log_trace(f"Rejected document {entry.source_paper_doi} due to low trust score: {trust_score.score}", {"penalties": trust_score.penalties_applied})
                    continue
                    
                raw_doc = ingestor.ingest_mock_pubmed(
                    pmid=entry.source_paper_doi,
                    title=entry.retriever_metadata.get("title", "Unknown Title"),
                    abstract=entry.claim_text,
                    year=year
                )
                raw_docs.append(raw_doc)
                
                docs.append({
                    "source_doi": raw_doc.external_id,
                    "text": f"{raw_doc.title} {raw_doc.abstract}",
                    "title": raw_doc.title,
                    "normalized_entities": raw_doc.normalized_entities,
                    "is_adversarial": is_adversarial,
                    "trust_score": getattr(trust_score, "model_dump", trust_score.dict)() if hasattr(trust_score, "dict") else trust_score,
                })
            return docs, raw_docs

        documents, raw_documents = process_entries(provenance_entries, is_adversarial=False)
        adv_documents, adv_raw_documents = process_entries(adv_provenance_entries, is_adversarial=True)
        
        # Merge supporting and adversarial evidence
        documents.extend(adv_documents)
        raw_documents.extend(adv_raw_documents)
            
        # Run Knowledge Graph Extraction (Compartment 1B pre-cursor)
        extractor = KnowledgeGraphExtractor(self.gateway)
        extracted_entities = []
        extracted_relations = []
        
        # We will keep track of raw Entity and Relationship objects for the Indexer
        raw_entity_objects = []
        raw_relationship_objects = []
        
        for doc in documents:
            kg = extractor.extract_from_text(doc["text"], doc["source_doi"])
            
            raw_entity_objects.extend(kg.entities)
            raw_relationship_objects.extend(kg.relationships)
            
            extracted_entities.extend([e.model_dump() for e in kg.entities])
            extracted_relations.extend([
                r.model_dump() | {"source_id": doc["source_doi"]} for r in kg.relationships
            ])
            
        # Execute Compartment 1B: Semantic & Topological Indexing
        indexer.index_entities_and_relationships(raw_entity_objects, raw_relationship_objects)

        session.knowledge_context = {
            "query": session.question, 
            "documents": documents,
            "extracted_graph": {
                "entities": extracted_entities,
                "relationships": extracted_relations
            }
        }
        return DiscoveryState.GAP_ANALYSIS


class GapAnalysisNode(WorkflowNode):
    def __init__(self) -> None:
        super().__init__("GapAnalysis")

    def execute(self, session: DiscoverySession) -> DiscoveryState:
        from aidp.discovery.contradiction import ContradictionDetectionEngine
        from aidp.knowledge.provenance import ProvenanceEntry
        from aidp.knowledge.world_model import ScientificEntity, ScientificRelationship, WorldModel
        from aidp.planning.router import DomainRouter

        session.log_trace("Starting protocol synthesis")
        
        # 1. Determine the domain
        router = DomainRouter()
        domain = router.route(session.question, session.knowledge_context)
        session.log_trace(f"Routed query to domain: {domain.value}")
        session.knowledge_context["domain"] = domain.value
        
        # 2. Extract facts from retrieved literature
        world_model = WorldModel()
        graph_data = session.knowledge_context.get("extracted_graph", {})
        
        for e in graph_data.get("entities", []):
            world_model.add_entity(ScientificEntity(
                name=e.get("name"),
                semantic_type=e.get("semantic_type")
            ))
            
        for r in graph_data.get("relationships", []):
            source_ent = world_model.get_entity_by_name(r.get("source_entity_name"))
            target_ent = world_model.get_entity_by_name(r.get("target_entity_name"))
            if source_ent and target_ent:
                world_model.add_relationship(ScientificRelationship(
                    source_entity_id=source_ent.id,
                    target_entity_id=target_ent.id,
                    relation_type=r.get("relation_type"),
                    is_causal=r.get("is_causal", False),
                    provenance=ProvenanceEntry(
                        source_paper_doi=r.get("source_id", "unknown"),
                        claim_text="",
                        source_url="",
                        retriever_metadata={},
                        confidence_score=1.0
                    )
                ))

        engine = ContradictionDetectionEngine()
        session.contradictions = engine.scan_for_contradictions(world_model)
        
        if not session.contradictions:
             session.contradictions = [
                {"id": "c1", "description": f"No direct contradictions found. Gap: Need to investigate {session.question}"}
             ]
             
        return DiscoveryState.HYPOTHESIS


class HypothesisNode(WorkflowNode):
    def __init__(self, gateway: IntelligenceGateway) -> None:
        super().__init__("HypothesisGeneration")
        self.generator = HypothesisGenerator(gateway=gateway)

    def execute(self, session: DiscoverySession) -> DiscoveryState:
        from aidp.governance.engine import ScientificGovernanceEngine
        session.log_trace("Entering Hypothesis Generation")
        if not session.contradictions:
            session.contradictions = [
                {"id": "c1", "description": f"No direct contradictions found. Gap: Need to investigate {session.question}"}
            ]

        contradiction = session.contradictions[0]
        hypotheses = self.generator.generate_from_contradiction(contradiction, session.knowledge_context)
        if not hypotheses:
            raise RuntimeError("Hypothesis generator returned no hypotheses. Transient failure?")
        session.hypothesis = hypotheses[0]
        
        # Run Governance Check
        gov_engine = ScientificGovernanceEngine()
        passed, gov_msg = gov_engine.evaluate_hypothesis(session.hypothesis)
        if not passed:
            session.log_trace("Governance Rejected Hypothesis", {"reason": gov_msg})
            # Drop confidence to 0.0 effectively by forcing failure
            return DiscoveryState.FAILED

        return DiscoveryState.PLANNING


class PlanningNode(WorkflowNode):
    def __init__(self, gateway: IntelligenceGateway, ablation_config: AblationConfig | None = None) -> None:
        super().__init__("ExperimentPlanning")
        self.gateway = gateway
        self.ablation_config = ablation_config or AblationConfig()
        
        # Instantiate detector, router, and ledger
        self.detector = DomainDetector(planner=WetLabPlanner(gateway=gateway).planner) # Reuse planner for detector
        self.router = DomainRouter(gateway=gateway)
        self.ledger = EpistemicLedger()

    def execute(self, session: DiscoverySession) -> DiscoveryState:
        session.log_trace("Entering Experiment Planning")
        if not session.hypothesis:
            return DiscoveryState.FAILED
            
        if not self.ablation_config.enable_spl:
            # Baseline Mode: Skip SPL, use raw hypothesis as experimental design
            session.log_trace("SPL Ablated: Using raw hypothesis")
            session.experiment_design = {"baseline_output": session.hypothesis.get("rationale", "No output generated")}
            return DiscoveryState.REVIEW

        # Detect domain
        domain = self.detector.detect_domain(
            hypothesis_claim=session.hypothesis.get("claim", ""),
            query=session.question
        )
        session.log_trace(f"Domain Detected: {domain.value}")
        
        # Route to appropriate planner
        planner = self.router.get_planner(domain)
        
        # Inject ablation config if applicable (both planners support this)
        if hasattr(planner, 'ablation_config'):
            planner.ablation_config = self.ablation_config

        ledger_entry = {"id": f"l_{uuid.uuid4()}", "readiness": "readyForExperiment"}
        design = planner.design_experiment(session.hypothesis, ledger_entry, session.knowledge_context)
        
        # Run Domain Metrics Validation
        from aidp.planning.metrics import DomainMetricValidator
        validator = DomainMetricValidator()
        validation_result = validator.validate_design(design)
        if not validation_result["valid"]:
            session.log_trace("Planning failed domain structural validation.", {"penalties": validation_result["penalties"]})
            return DiscoveryState.FAILED
            
        session.experiment_design = design
        
        # Build Epistemic Evidence
        evidence_list = []
        for doc in session.knowledge_context.get("documents", []):
            evidence_list.append(
                EpistemicEvidence(
                    source_id=doc.get("source_doi", "unknown"),
                    source_type="literature",
                    extracted_text=doc.get("text", ""),
                    relevance_score=1.0
                )
            )
            
        # Build initial Epistemic Claim
        claim = EpistemicClaim(
            claim_text=session.hypothesis.get("claim", "No claim provided"),
            evidence=evidence_list,
            assumptions=design.get("assumptions", []),
            generated_by=planner.__class__.__name__
        )
        self.ledger.append_claim(claim)
        
        # Store claim ID in session so ReviewNode can update it
        session.experiment_design["epistemic_claim_id"] = claim.claim_id
        
        return DiscoveryState.FORMAL_VERIFICATION


class VerificationNode(WorkflowNode):
    def __init__(self) -> None:
        super().__init__("FormalVerification")
        
    def execute(self, session: DiscoverySession) -> DiscoveryState:
        from aidp.verification.verification_engine import FormalVerificationEngine
        
        session.log_trace("Entering Formal Verification")
        if not session.experiment_design:
            return DiscoveryState.FAILED
            
        # Optional: Hydrate world model for assumption solver if available
        # But we'll just pass a basic instance or None for now.
        engine = FormalVerificationEngine(world_model=None) 
        
        report = engine.run(session.experiment_design)
        
        session.telemetry["verification_report"] = report
        
        if report["status"] == "FAILED":
            session.log_trace("Formal Verification FAILED", {"reason": report.get("blocking_reason")})
            
            # RLHF: Penalize the Planning Agent in the Academy
            from aidp.meta_learning.academy import AutonomousResearchAcademy
            from aidp.meta_learning.skill_graph import ScientificSkillGraph
            academy = AutonomousResearchAcademy(skill_graph=ScientificSkillGraph())
            academy.penalize_agent_for_failure("planner_agent", "formal_verification_failure", penalty=0.3)
            
            # Log catastrophic verification failure to memory
            from aidp.memory.failure_memory import FailureMemoryManager
            fm = FailureMemoryManager()
            fm.log_failure(
                session_id=session.id,
                failure_type="VERIFICATION_REJECTION",
                domain="WetLab", # Hardcoded for now, could dynamically resolve
                context={"hypothesis": session.hypothesis.get("claim", ""), "design": session.experiment_design},
                critique=f"Verification Failed: {report.get('blocking_reason')}"
            )
            # We fail out strictly, rather than letting the LLM guess again.
            return DiscoveryState.FAILED
            
        session.log_trace("Formal Verification PASSED")
        return DiscoveryState.REVIEW

class ReviewNode(WorkflowNode):
    def __init__(self, gateway: IntelligenceGateway, requires_human_approval: bool = False) -> None:
        super().__init__("ScientificReview")
        self.debate_engine = ScientificDebateEngine(gateway=gateway)
        self.calibrator = ConfidenceCalibrator()
        self.lineage_engine = LineageEngine()
        self.ledger = EpistemicLedger()
        self.requires_human_approval = requires_human_approval

    def execute(self, session: DiscoverySession) -> DiscoveryState:
        session.log_trace("Entering Scientific Review")
        if not session.experiment_design or not session.hypothesis:
            return DiscoveryState.FAILED

        record = self.debate_engine.evaluate_design(session.experiment_design, session.hypothesis)
        session.debate_record = record
        
        if self.requires_human_approval:
            session.log_trace("Pausing for human review...")
            return DiscoveryState.PAUSED
            
        return self._finalize_review(session, record)
        
    def on_event(self, session: DiscoverySession, event_data: dict[str, Any]) -> DiscoveryState:
        if event_data.get("type") == "HUMAN_REVIEW_EVENT":
            decision = event_data.get("decision", "Reject")
            feedback = event_data.get("feedback", "No feedback provided")
            session.log_trace("Human review received", {"decision": decision})
            
            # Append human critique to debate record
            session.debate_record.setdefault("critiques", []).append({
                "role": "Human PI",
                "decision": decision,
                "evidence": feedback,
                "blockingIssues": [feedback] if decision != "Approve" else []
            })
            
            if decision == "Approve":
                session.debate_record["consensusReached"] = True
                session.debate_record["consensusReport"] = {"summary": "Approved by Human PI."}
            else:
                session.debate_record["consensusReached"] = False
                
            return self._finalize_review(session, session.debate_record)
            
        raise ValueError(f"Unknown event type for ReviewNode: {event_data.get('type')}")

    def _finalize_review(self, session: DiscoverySession, record: dict[str, Any]) -> DiscoveryState:
        # Fetch the original claim
        claim_id = session.experiment_design.get("epistemic_claim_id")
        claim = self.ledger.get_claim_by_id(claim_id) if claim_id else None
        
        if claim:
            reviews = []
            approve_count = 0
            total_count = 0
            for critique in record.get("critiques", []):
                vote_str = critique.get("decision", "abstain").lower()
                total_count += 1
                if vote_str == "approve":
                    approve_count += 1
                    
                reviews.append(
                    EpistemicReview(
                        reviewer_role=critique.get("role", "Reviewer"),
                        vote=critique.get("decision", "Abstain"),
                        rationale=critique.get("evidence", "No rationale"),
                        identified_confounds=critique.get("blockingIssues", [])
                    )
                )
            
            claim.reviewed_by = reviews
            
            # Fetch the verification report if it exists in telemetry
            ver_report = session.telemetry.get("verification_report", {"status": "PASS"})
            
            # Save old ontology for lineage tracking
            old_ontology = claim.confidence

            # Calibrate Confidence Ontology
            new_ontology = self.calibrator.calibrate(
                claim=claim,
                debate_record=record,
                verification_report=ver_report
            )
            
            # Track Lineage
            lineage_events = self.lineage_engine.generate_lineage(old_ontology, new_ontology)
            
            # Apply updates
            claim.confidence = new_ontology
            claim.confidence_lineage.extend(lineage_events)
            
            # Map ConfidenceLevel to VerificationStatus
            if new_ontology.verification_confidence == 0.0:
                claim.verification_status = VerificationStatus.REJECTED
            elif new_ontology.overall_confidence >= 0.8:
                claim.verification_status = VerificationStatus.VERIFIED
            elif new_ontology.overall_confidence >= 0.5:
                claim.verification_status = VerificationStatus.UNCERTAIN
            else:
                claim.verification_status = VerificationStatus.REJECTED
                
            # Log the resolved claim
            self.ledger.append_claim(claim)
            
            session.telemetry["final_confidence_ontology"] = new_ontology.model_dump()
            session.telemetry["lineage_events_generated"] = len(lineage_events)
        
        # Determine next state based on claim's verification status
        if claim and claim.verification_status == VerificationStatus.VERIFIED:
            session.consensus_report = record.get("consensusReport", {})
            return DiscoveryState.APPROVED
        elif not claim and record.get("consensusReached"):
            # Fallback if ledger was disabled/failed
            session.consensus_report = record.get("consensusReport", {})
            return DiscoveryState.APPROVED
        else:
            return DiscoveryState.FAILED


class MemoryUpdateNode(WorkflowNode):
    def __init__(self) -> None:
        super().__init__("MemoryUpdate")

    def execute(self, session: DiscoverySession) -> DiscoveryState:
        from aidp.memory.decision_memory import DecisionMemoryManager
        from aidp.memory.evidence_memory import EvidenceMemoryManager
        from aidp.memory.experiment_memory import ExperimentMemoryManager
        from aidp.memory.failure_memory import FailureMemoryManager
        
        session.log_trace("Entering Memory Update")
        
        dm = DecisionMemoryManager()
        fm = FailureMemoryManager()
        exm = ExperimentMemoryManager()
        evm = EvidenceMemoryManager()
        
        # Determine if we had a success or failure
        if session.consensus_report:
            # We reached an approval
            
            # Reconstruct confidence breakdown from ledger if possible
            claim_id = session.experiment_design.get("epistemic_claim_id")
            ledger = EpistemicLedger()
            claim = ledger.get_claim_by_id(claim_id) if claim_id else None
            confidence_breakdown = claim.confidence.model_dump() if claim and claim.confidence else {}
            
            dm.log_decision(
                session_id=session.id,
                context=f"Hypothesis: {session.hypothesis.get('claim', '')}",
                decision="Consensus Approved",
                rationale="Reviewers agreed with the experimental design.",
                confidence_breakdown=confidence_breakdown
            )
            
            # Log successful experiment design
            exm.log_experiment(
                session_id=session.id,
                domain="WetLab",
                experiment_design=session.experiment_design
            )
            
            # Log highly confident evidence
            if claim and claim.evidence:
                evm.log_evidence(
                    session_id=session.id,
                    claim_id=claim.claim_id,
                    evidence_list=[e.model_dump() for e in claim.evidence] if claim else []
                )
                
        elif session.debate_record and not session.debate_record.get("consensusReached"):
            # We failed debate
            critiques = [c.get('blockingIssues') for c in session.debate_record.get('critiques', []) if c.get('decision') == 'Reject']
            fm.log_failure(
                session_id=session.id,
                failure_type="DEBATE_REJECTION",
                domain="WetLab",
                context={"hypothesis": session.hypothesis.get("claim", ""), "design": session.experiment_design},
                critique=str(critiques)
            )
            
        return DiscoveryState.EXECUTION


class ExecutionNode(WorkflowNode):
    def __init__(self) -> None:
        super().__init__("Execution")

    def execute(self, session: DiscoverySession) -> DiscoveryState:
        from aidp.intelligence.compilers import AutoprotocolCompiler, PyRosettaCompiler
        
        session.log_trace("Entering Execution Compilation")
        design = session.experiment_design
        domain = session.telemetry.get("domain", "Unknown")
        
        if domain == "WET_LAB":
            compiler = AutoprotocolCompiler()
            compiled_code = compiler.compile(design)
            session.telemetry["compiled_autoprotocol"] = compiled_code
        elif domain == "COMPUTATIONAL":
            compiler = PyRosettaCompiler()
            compiled_code = compiler.compile(design)
            session.telemetry["compiled_pyrosetta"] = compiled_code
            
        return DiscoveryState.FINISHED


# --- DAG Orchestrator ---


class WorkflowDAG:
    def __init__(self) -> None:
        self.nodes: dict[DiscoveryState, WorkflowNode] = {}
        self.max_retries = 3

    def register_node(self, state: DiscoveryState, node: WorkflowNode) -> None:
        self.nodes[state] = node

    def execute(self, session: DiscoverySession, resume: bool = False) -> DiscoverySession:
        start_time = time.time()
        session.telemetry["start_time"] = start_time

        if not resume or session.state == DiscoveryState.INIT:
            session.state = DiscoveryState.RETRIEVAL

        while session.state not in (DiscoveryState.FINISHED, DiscoveryState.FAILED, DiscoveryState.PAUSED):
            node = self.nodes.get(session.state)
            if not node:
                session.log_trace("No node registered for state", {"state": session.state.value})
                session.state = DiscoveryState.FAILED
                break

            retries = 0
            success = False
            next_state = DiscoveryState.FAILED

            while retries < self.max_retries and not success:
                try:
                    next_state = node.execute(session)
                    success = True
                except Exception as e:
                    retries += 1
                    session.log_trace(
                        f"Node Execution Exception ({retries}/{self.max_retries})",
                        {"error": str(e), "node": node.name},
                    )
                    raise e

            if not success:
                session.state = DiscoveryState.FAILED
                break

            if next_state == DiscoveryState.PAUSED:
                session.paused_at_state = session.state.value

            session.state = next_state
            # Checkpoint after every successful stage
            try:
                session.save_checkpoint()
            except Exception as e:
                session.log_trace("Checkpoint Save Failed", {"error": str(e)})

        session.telemetry["end_time"] = time.time()
        session.telemetry["total_runtime_seconds"] = session.telemetry.get("total_runtime_seconds", 0) + (session.telemetry["end_time"] - start_time)
        session.log_trace("Workflow Exited Loop", {"final_state": session.state.value})

        return session


class AutonomousDiscoveryOrchestrator:
    """Top level facade for running discovery workflows."""

    def __init__(self, gateway: IntelligenceGateway, ablation_config: AblationConfig | None = None, requires_human_approval: bool = False) -> None:
        self.gateway = gateway
        self.ablation_config = ablation_config or AblationConfig()
        self.dag = WorkflowDAG()

        self.dag.register_node(DiscoveryState.RETRIEVAL, RetrievalNode(self.gateway))
        self.dag.register_node(DiscoveryState.GAP_ANALYSIS, GapAnalysisNode())
        self.dag.register_node(DiscoveryState.HYPOTHESIS, HypothesisNode(self.gateway))
        self.dag.register_node(DiscoveryState.PLANNING, PlanningNode(self.gateway, self.ablation_config))
        self.dag.register_node(DiscoveryState.FORMAL_VERIFICATION, VerificationNode())
        self.dag.register_node(DiscoveryState.REVIEW, ReviewNode(self.gateway, requires_human_approval=requires_human_approval))
        self.dag.register_node(DiscoveryState.APPROVED, MemoryUpdateNode())
        self.dag.register_node(DiscoveryState.EXECUTION, ExecutionNode())

    def run_discovery_cycle(self, question: str, historical_cutoff_date: str | None = None) -> DiscoverySession:
        session = DiscoverySession(question=question, historical_cutoff_date=historical_cutoff_date)
        return self.dag.execute(session)

    def resume_discovery_cycle(self, checkpoint_path: str) -> DiscoverySession:
        session = DiscoverySession.load_checkpoint(checkpoint_path)
        return self.dag.execute(session, resume=True)

    def resume_from_event(self, checkpoint_path: str, event_data: dict[str, Any]) -> DiscoverySession:
        """
        Resumes a PAUSED workflow by injecting an external event into the node currently responsible for the state.
        """
        session = DiscoverySession.load_checkpoint(checkpoint_path)
        if session.state != DiscoveryState.PAUSED:
            raise ValueError(f"Cannot resume from event: Session {session.id} is not PAUSED (current state: {session.state.value}).")
        
        if not session.paused_at_state:
            raise ValueError("Session is PAUSED but lacks a paused_at_state to resume from.")
            
        origin_state = DiscoveryState(session.paused_at_state)
        node = self.dag.nodes.get(origin_state)
        
        if not node:
            raise ValueError(f"No node registered for original state {origin_state}")
            
        session.log_trace("Resuming from event", {"event_type": event_data.get("type", "unknown")})
        next_state = node.on_event(session, event_data)
        
        if next_state == DiscoveryState.PAUSED:
            # Re-paused
            pass
        else:
            session.paused_at_state = None
            session.event_payload = {}
            
        session.state = next_state
        session.save_checkpoint()
        
        return self.dag.execute(session, resume=True)

    def generate_report(self, session: DiscoverySession) -> str:
        """Compiles the discovery session into a publishable markdown report."""
        report = f"# Discovery Report: {session.question}\n\n"
        report += f"**Final State:** {session.state.value}\n\n"

        report += "## 1. Contradictions Identified\n"
        for c in session.contradictions:
            report += f"- {c.get('description', 'Unknown')}\n"

        report += "\n## 2. Hypothesis\n"
        if session.hypothesis:
            report += f"**Claim:** {session.hypothesis.get('claim')}\n"
            report += f"**Rationale:** {session.hypothesis.get('rationale')}\n"

        report += "\n## 3. Experimental Design\n"
        if session.experiment_design:
            report += f"- **Independent Variables:** {session.experiment_design.get('independentVariables', [])}\n"
            report += f"- **Dependent Variables:** {session.experiment_design.get('dependentVariables', [])}\n"
            report += f"- **Controls:** {session.experiment_design.get('controls', [])}\n"

        report += "\n## 4. Scientific Review & Consensus\n"
        if session.debate_record:
            report += f"**Consensus Reached:** {session.debate_record.get('consensusReached')}\n"
            for critique in session.debate_record.get('critiques', []):
                report += f"- **{critique.get('role')}**: Decision={critique.get('decision')}, BlockingIssues={critique.get('blockingIssues')}\n"

        report += "\n## 5. Telemetry\n"
        report += f"**Runtime:** {session.telemetry.get('total_runtime_seconds', 0):.2f}s\n"

        return report
