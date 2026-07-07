import json
import uuid
from typing import Optional, Any

from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.reasoning_planner import ReasoningPlanner
from aidp.intelligence.task_specification import CognitiveTaskType, TaskSpecification


class HypothesisGenerator:
    """
    Synthesizes competing hypotheses bridging isolated knowledge gaps or resolving contradictions.
    """

    def __init__(self, gateway: Optional[IntelligenceGateway] = None) -> None:
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

    def generate_from_contradiction(self, contradiction: dict[str, Any]) -> list[dict[str, Any]]:
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
                    "confidence": 0.6,
                    "risk": 0.3,
                    "expectedInformationGain": contradiction.get("contradictionScore", 1.0) * 0.95,
                }
                hypotheses.append(h1)
            return hypotheses

        schema_hint = {"claim": None, "rationale": None, "confidence_prior": None}

        spec = TaskSpecification(
            task_type=CognitiveTaskType.HYPOTHESIS_GENERATION,
            context={"contradiction": json.dumps(contradiction)},
            expected_schema=schema_hint,
            strict_falsifiability=True,
        )

        try:
            result = self.planner.execute_task(spec) if self.planner else {}
            h_new = {
                "id": f"hyp-{uuid.uuid4()}",
                "claim": result.get("claim", "Failed to generate claim."),
                "rationale": result.get("rationale", ""),
                "supportingEvidenceIds": [
                    contradiction.get("sourceAId"),
                    contradiction.get("sourceBId"),
                ],
                "opposingEvidenceIds": [],
                "confidence": result.get("confidence_prior", 0.5),
                "risk": 1.0 - result.get("confidence_prior", 0.5),
                "expectedInformationGain": contradiction.get("contradictionScore", 1.0) * 0.95,
            }
            hypotheses.append(h_new)
        except Exception as e:
            print(f"Failed to generate hypothesis: {e}")

        return hypotheses
