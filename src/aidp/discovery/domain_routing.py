from enum import Enum

from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.reasoning_planner import ReasoningPlanner
from aidp.intelligence.task_specification import CognitiveTaskType, TaskSpecification


class ScientificDomain(Enum):
    WET_LAB = "WET_LAB"
    CLINICAL_TRIAL = "CLINICAL_TRIAL"
    MATERIALS = "MATERIALS"
    COMPUTATIONAL = "COMPUTATIONAL"
    OBSERVATIONAL = "OBSERVATIONAL"
    UNKNOWN = "UNKNOWN"

class DomainDetector:
    def __init__(self, planner: ReasoningPlanner | None) -> None:
        self.planner = planner

    def detect_domain(self, hypothesis_claim: str, query: str) -> ScientificDomain:
        if not self.planner:
            return ScientificDomain.WET_LAB

        schema_hint = {
            "domain": "string (WET_LAB, CLINICAL_TRIAL, MATERIALS, COMPUTATIONAL, OBSERVATIONAL)",
            "justification": "string"
        }

        context = {
            "hypothesis": hypothesis_claim,
            "claim": hypothesis_claim,
            "success_criteria": "Determine the optimal experimental domain",
            "variables": "None",
            "query": query
        }

        spec = TaskSpecification(
            task_type=CognitiveTaskType.FALSIFIABILITY_GENERATION, # Reusing this cognitive task type for now as it handles strict structured output
            context=context,
            expected_schema=schema_hint,
            strict_falsifiability=False
        )

        # We override the actual prompt dynamically via the gateway or task spec in a real system,
        # but for simplicity we rely on the planner's generic capability and the schema hint.
        # Let's augment the context to instruct domain detection.
        spec.context["INSTRUCTION"] = "Classify the scientific domain of the given hypothesis and query. Choose exactly one from: WET_LAB, CLINICAL_TRIAL, MATERIALS, COMPUTATIONAL, OBSERVATIONAL."

        result = self.planner.execute_task(spec)
        domain_str = result.get("domain", "").upper()
        
        try:
            return ScientificDomain(domain_str)
        except ValueError:
            # Simple fuzzy matching fallback
            if "CLINICAL" in domain_str or "PATIENT" in domain_str:
                return ScientificDomain.CLINICAL_TRIAL
            return ScientificDomain.WET_LAB

class DomainRouter:
    def __init__(self, gateway: IntelligenceGateway) -> None:
        self.gateway = gateway

    def get_planner(self, domain: ScientificDomain):
        if domain == ScientificDomain.CLINICAL_TRIAL:
            from aidp.discovery.clinical_planning import ClinicalTrialPlanner
            return ClinicalTrialPlanner(self.gateway)
        elif domain == ScientificDomain.COMPUTATIONAL:
            from aidp.discovery.computational_planning import ComputationalPlanner
            return ComputationalPlanner(self.gateway)
        else:
            # Default to Wet Lab
            from aidp.discovery.scientific_planning import WetLabPlanner
            return WetLabPlanner(self.gateway)
