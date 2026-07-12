import json
import os
import time
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Optional, Any

from aidp.discovery.debate import ScientificDebateEngine
from aidp.discovery.scientific_planning import ScientificPlanningLayer
from aidp.discovery.hypothesis import HypothesisGenerator
from aidp.intelligence.providers.middleware import IntelligenceGateway


class DiscoveryState(Enum):
    INIT = "INIT"
    RETRIEVAL = "RETRIEVAL"
    GAP_ANALYSIS = "GAP_ANALYSIS"
    HYPOTHESIS = "HYPOTHESIS"
    PLANNING = "PLANNING"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    MEMORY_UPDATE = "MEMORY_UPDATE"
    FINISHED = "FINISHED"
    FAILED = "FAILED"


@dataclass
class DiscoverySession:
    id: str = field(default_factory=lambda: f"sess_{uuid.uuid4()}")
    question: str = ""
    historical_cutoff_date: Optional[str] = None
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

    def log_trace(self, event: str, metadata: Optional[dict[str, Any]] = None) -> None:
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
        """
        raise NotImplementedError


# --- Node Implementations ---


class RetrievalNode(WorkflowNode):
    def __init__(self) -> None:
        super().__init__("KnowledgeRetrieval")

    def execute(self, session: DiscoverySession) -> DiscoveryState:
        from aidp.knowledge.connectors.pubmed_connector import PubMedConnector
        from dataclasses import asdict
        
        session.log_trace("Entering Knowledge Retrieval")
        
        connector = PubMedConnector(max_results=3)
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

        provenance_entries = connector.fetch_literature_provenance(search_term, max_date=max_date)
        
        # Query Fallback Strategy: if the highly specific semantic query returns 0 results, 
        # fall back to a broader entity-only query.
        if len(provenance_entries) == 0:
            session.log_trace("Semantic query returned 0 results. Falling back to entity query.", {"failed_query": search_term})
            fallback_term = " ".join([w for w in session.question.replace('?','').split() if any(c.isupper() for c in w)])
            if fallback_term:
                provenance_entries = connector.fetch_literature_provenance(fallback_term, max_date=max_date)
        
        documents = []
        for entry in provenance_entries:
            documents.append({
                "source_doi": entry.source_paper_doi,
                "text": entry.claim_text,
                "title": entry.retriever_metadata.get("title")
            })
            
        session.knowledge_context = {
            "query": session.question, 
            "documents": documents
        }
        return DiscoveryState.GAP_ANALYSIS


class GapAnalysisNode(WorkflowNode):
    def __init__(self) -> None:
        super().__init__("GapAnalysis")

    def execute(self, session: DiscoverySession) -> DiscoveryState:
        session.log_trace("Entering Gap Analysis")
        # Extract contradiction from knowledge context
        session.contradictions = [
            {"id": "c1", "description": f"Contradiction related to {session.question}"}
        ]
        return DiscoveryState.HYPOTHESIS


class HypothesisNode(WorkflowNode):
    def __init__(self, gateway: IntelligenceGateway) -> None:
        super().__init__("HypothesisGeneration")
        self.generator = HypothesisGenerator(gateway=gateway)

    def execute(self, session: DiscoverySession) -> DiscoveryState:
        session.log_trace("Entering Hypothesis Generation")
        if not session.contradictions:
            return DiscoveryState.FAILED

        contradiction = session.contradictions[0]
        hypotheses = self.generator.generate_from_contradiction(contradiction, session.knowledge_context)
        if not hypotheses:
            raise RuntimeError("Hypothesis generator returned no hypotheses. Transient failure?")
        session.hypothesis = hypotheses[0]
        return DiscoveryState.PLANNING


class PlanningNode(WorkflowNode):
    def __init__(self, gateway: IntelligenceGateway) -> None:
        super().__init__("ExperimentPlanning")
        self.planner = ScientificPlanningLayer(gateway=gateway)

    def execute(self, session: DiscoverySession) -> DiscoveryState:
        session.log_trace("Entering Experiment Planning")
        if not session.hypothesis:
            return DiscoveryState.FAILED

        ledger_entry = {"id": f"l_{uuid.uuid4()}", "readiness": "readyForExperiment"}
        design = self.planner.design_experiment(session.hypothesis, ledger_entry, session.knowledge_context)
        session.experiment_design = design
        return DiscoveryState.REVIEW


class ReviewNode(WorkflowNode):
    def __init__(self, gateway: IntelligenceGateway) -> None:
        super().__init__("ScientificReview")
        self.debate_engine = ScientificDebateEngine(gateway=gateway)

    def execute(self, session: DiscoverySession) -> DiscoveryState:
        session.log_trace("Entering Scientific Review")
        if not session.experiment_design or not session.hypothesis:
            return DiscoveryState.FAILED

        record = self.debate_engine.evaluate_design(session.experiment_design, session.hypothesis)
        session.debate_record = record
        if record.get("consensusReached"):
            session.consensus_report = record.get("consensusReport", {})
            return DiscoveryState.APPROVED
        else:
            return DiscoveryState.FAILED


class MemoryUpdateNode(WorkflowNode):
    def __init__(self) -> None:
        super().__init__("MemoryUpdate")

    def execute(self, session: DiscoverySession) -> DiscoveryState:
        session.log_trace("Entering Memory Update")
        # In the future, write to procedural and knowledge memory
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

        while session.state not in (DiscoveryState.FINISHED, DiscoveryState.FAILED):
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
                    time.sleep(1)  # Backoff

            if not success:
                session.state = DiscoveryState.FAILED
                break

            session.state = next_state
            # Checkpoint after every successful stage
            try:
                session.save_checkpoint()
            except Exception as e:
                session.log_trace("Checkpoint Save Failed", {"error": str(e)})

        session.telemetry["end_time"] = time.time()
        session.telemetry["total_runtime_seconds"] = session.telemetry["end_time"] - start_time
        session.log_trace("Workflow Terminated", {"final_state": session.state.value})

        return session


class AutonomousDiscoveryOrchestrator:
    """Top level facade for running discovery workflows."""

    def __init__(self, gateway: IntelligenceGateway) -> None:
        self.gateway = gateway
        self.dag = WorkflowDAG()

        self.dag.register_node(DiscoveryState.RETRIEVAL, RetrievalNode())
        self.dag.register_node(DiscoveryState.GAP_ANALYSIS, GapAnalysisNode())
        self.dag.register_node(DiscoveryState.HYPOTHESIS, HypothesisNode(self.gateway))
        self.dag.register_node(DiscoveryState.PLANNING, PlanningNode(self.gateway))
        self.dag.register_node(DiscoveryState.REVIEW, ReviewNode(self.gateway))
        self.dag.register_node(DiscoveryState.APPROVED, MemoryUpdateNode())

    def run_discovery_cycle(self, question: str, historical_cutoff_date: Optional[str] = None) -> DiscoverySession:
        session = DiscoverySession(question=question, historical_cutoff_date=historical_cutoff_date)
        return self.dag.execute(session)

    def resume_discovery_cycle(self, checkpoint_path: str) -> DiscoverySession:
        session = DiscoverySession.load_checkpoint(checkpoint_path)
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
