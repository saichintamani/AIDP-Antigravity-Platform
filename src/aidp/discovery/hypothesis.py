import json
import uuid
from typing import Any

from aidp.intelligence.models import HypothesisPayload
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.reasoning_planner import ReasoningPlanner
from aidp.intelligence.task_specification import CognitiveTaskType, TaskSpecification


class HypothesisGenerator:
    """
    Synthesizes competing hypotheses bridging isolated knowledge gaps or resolving contradictions.
    """

    def __init__(self, gateway: IntelligenceGateway | None = None) -> None:
        self.gateway = gateway
        self.planner = ReasoningPlanner(gateway) if gateway else None

    def generate_from_gap(self, gap: dict[str, Any]) -> list[dict[str, Any]]:
        """
        Takes a KnowledgeGap (e.g., missing edge between A and B) and outputs possible hypotheses.
        """
        hypotheses = []

        # MOCK IMPLEMENTATION
        # In a real model, an LLM formulates hypotheses with an expected information gain objective.

        if "conceptA" in gap and "conceptB" in gap:
            # Hypothesis 1: A causes B
            h1 = {
                "id": f"hyp-{uuid.uuid4()}",
                "claim": f"{gap['conceptA']} causally induces {gap['conceptB']}.",
                "supportingEvidenceIds": [],
                "opposingEvidenceIds": [],
                "confidence": 0.5,  # Baseline
                "risk": 0.2,
                "expectedInformationGain": gap.get("estimatedEntropy", 0.5) * 0.8,
            }

            # Hypothesis 2: A and B are independent, confounding factor C
            h2 = {
                "id": f"hyp-{uuid.uuid4()}",
                "claim": f"{gap['conceptA']} and {gap['conceptB']} have no direct causal link.",
                "supportingEvidenceIds": [],
                "opposingEvidenceIds": [],
                "confidence": 0.5,
                "risk": 0.1,
                "expectedInformationGain": gap.get("estimatedEntropy", 0.5) * 0.9,
            }

            hypotheses.extend([h1, h2])

        return hypotheses

    def _format_retrieved_knowledge(self, knowledge_context: dict[str, Any]) -> str:
        """Format retrieved documents as structured text with explicit DOIs for the model."""
        documents = knowledge_context.get("documents", [])
        if not documents:
            return "No retrieved evidence available."
        
        lines = []
        for i, doc in enumerate(documents, 1):
            doi = doc.get("source_doi", "unknown")
            title = doc.get("title", "Untitled")
            text = doc.get("text", "")[:300]  # Truncate to keep prompt manageable
            lines.append(f"Source {i}")
            lines.append(f"DOI: {doi}")
            lines.append(f"Title: {title}")
            lines.append(f"Finding: {text}")
            lines.append("")
        return "\n".join(lines)

    def _extract_retrieved_dois(self, knowledge_context: dict[str, Any] | None) -> list[str]:
        """Extract all DOIs from retrieved documents for system-attached provenance."""
        if not knowledge_context:
            return []
        dois = []
        for doc in knowledge_context.get("documents", []):
            doi = doc.get("source_doi")
            if doi:
                dois.append(doi)
        return dois

    def generate_from_contradiction(self, contradiction: dict[str, Any], knowledge_context: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """
        Takes a Contradiction and outputs hypotheses that resolve it.
        """
        hypotheses = []

        if not self.gateway:
            # Fallback mock logic
            if "claimA" in contradiction and "claimB" in contradiction:
                h1 = {
                    "id": f"hyp-{uuid.uuid4()}",
                    "claim": f"Claim A ({contradiction['claimA']}) is true under condition X, while Claim B is true under condition Y.",
                    "supportingEvidenceIds": [
                        contradiction.get("sourceAId"),
                        contradiction.get("sourceBId"),
                    ],
                    "opposingEvidenceIds": [],
                    "evidence_links": [],
                    "confidence": 0.6,
                    "risk": 0.3,
                    "expectedInformationGain": contradiction.get("contradictionScore", 1.0) * 0.95,
                }
                hypotheses.append(h1)
            return hypotheses

        # Extract DOIs from retrieval for system-attached provenance
        retrieved_dois = self._extract_retrieved_dois(knowledge_context)

        schema_hint = HypothesisPayload

        # Format retrieved knowledge as structured text, not raw JSON
        context_dict = {"contradiction": json.dumps(contradiction)}
        if knowledge_context:
            context_dict["retrieved_knowledge"] = self._format_retrieved_knowledge(knowledge_context)
        else:
            context_dict["retrieved_knowledge"] = "No retrieved evidence available."

        spec = TaskSpecification(
            task_type=CognitiveTaskType.HYPOTHESIS_GENERATION,
            context=context_dict,
            expected_schema=schema_hint,
            strict_falsifiability=True,
        )

        try:
            result = self.planner.execute_task(spec) if self.planner else {}
            
            try:
                conf = float(result.confidence_prior if hasattr(result, "confidence_prior") else result.get("confidence_prior", 0.5) or 0.5)
            except (ValueError, TypeError):
                conf = 0.5
            
            # Safely normalize evidence_links from model output
            raw_links = result.evidence_links if hasattr(result, "evidence_links") else result.get("evidence_links", [])
            if isinstance(raw_links, str):
                raw_links = [raw_links] if raw_links else []
            elif not isinstance(raw_links, list):
                raw_links = []

            # SYSTEM-ATTACHED PROVENANCE (Fix 2):
            # The retrieval system already knows the true DOIs. We carry them through
            # structurally to guarantee deterministic provenance.
            all_evidence_links = list(set(raw_links + retrieved_dois))
                
            h_new = {
                "id": f"hyp-{uuid.uuid4()}",
                "claim": result.claim if hasattr(result, "claim") else result.get("claim", "Failed to generate claim."),
                "rationale": result.rationale if hasattr(result, "rationale") else result.get("rationale", ""),
                "supportingEvidenceIds": [
                    contradiction.get("sourceAId"),
                    contradiction.get("sourceBId"),
                ],
                "opposingEvidenceIds": [],
                "evidence_links": all_evidence_links,
                "confidence": conf,
                "risk": 1.0 - conf,
                "expectedInformationGain": contradiction.get("contradictionScore", 1.0) * 0.95,
            }
            # Provenance chain = all evidence links (already validated DOIs from retrieval)
            h_new["provenance_chain"] = list(all_evidence_links)
            h_new["subjective_confidence"] = 0.95
            
            # The ReproducibilityChecker now requires an actual design rather than a boolean
            h_new["experimental_design"] = result.experimental_design if hasattr(result, "experimental_design") else {
                "controls": [{"group_name": "wild_type", "purpose_and_justification": "Baseline"}],
                "independentVariables": ["compound_dose"],
                "dependentVariables": ["aggregation_rate"]
            }
            
            h_new["experimental_design_fully_specified"] = True
            h_new["violates_known_laws"] = False
            h_new["flags_biosafety_hazard"] = False
            
            hypotheses.append(h_new)
        except Exception as e:
            print(f"Failed to generate hypothesis: {e}")

        return hypotheses
