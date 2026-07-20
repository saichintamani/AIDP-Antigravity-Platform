import uuid
from typing import Any

from aidp.discovery.scientific_planning import AblationConfig, BaseDomainPlanner
from aidp.intelligence.models import (
    ClinicalCohort,
    ClinicalMethodology,
    ClinicalSafetyEfficacy,
    ExecutionProtocolModel,
)
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.reasoning_planner import ReasoningPlanner
from aidp.intelligence.task_specification import CognitiveTaskType, TaskSpecification
from aidp.knowledge.connectors.pubmed_connector import PubMedConnector


class ClinicalMethodologyGenerator:
    def __init__(self, planner: ReasoningPlanner | None) -> None:
        self.planner = planner

    def generate(self, hypothesis: dict[str, Any], ablation_config: AblationConfig | None = None) -> dict[str, Any]:
        if not self.planner:
            return {
                "treatment_arms": ["Mock Treatment"],
                "comparator_arms": ["Mock Placebo"],
                "blinding_strategy": "Double-blind",
                "randomization": "1:1",
                "success_criteria": "Mock Endpoint Reached"
            }

        claim = hypothesis.get("claim", "")
        
        schema_hint = ClinicalMethodology

        if ablation_config and not ablation_config.enable_schema_sync:
            schema_hint = None

        spec = TaskSpecification(
            task_type=CognitiveTaskType.METHODOLOGY_GENERATION,
            context={"claim": claim, "evidence_mapping": "Clinical Evidence", "failure_memory": "None"},
            expected_schema=schema_hint,
            strict_falsifiability=True,
        )

        return self.planner.execute_task(spec)


class CohortSelectionValidator:
    def __init__(self, planner: ReasoningPlanner | None) -> None:
        self.planner = planner

    def validate(self, hypothesis_claim: str, methodology: dict[str, Any]) -> dict[str, Any]:
        if not self.planner:
            return {
                "inclusion_criteria": ["Mock Inclusion"],
                "exclusion_criteria": ["Mock Exclusion"],
                "demographic_considerations": "Mock Demo"
            }

        schema_hint = ClinicalCohort

        context = {
            "claim": hypothesis_claim,
            "methodology": str(methodology),
            "variables": "None",
            "confounders": "None"
        }

        spec = TaskSpecification(
            task_type=CognitiveTaskType.CONTROL_TAXONOMY_GENERATION, # Reusing
            context=context,
            expected_schema=schema_hint,
            strict_falsifiability=True,
        )

        spec.context["INSTRUCTION"] = "Define the cohort selection criteria for the clinical trial."

        return self.planner.execute_task(spec)


class SafetyAndEfficacyAnalyzer:
    def __init__(self, planner: ReasoningPlanner | None) -> None:
        self.planner = planner

    def analyze(self, methodology: dict[str, Any]) -> dict[str, Any]:
        if not self.planner:
            return {
                "primary_endpoints": ["Mock Primary"],
                "secondary_endpoints": ["Mock Secondary"],
                "safety_monitoring_plan": "Mock Safety Plan"
            }

        schema_hint = ClinicalSafetyEfficacy
        
        # Tool-Augmented Planning: Retrieve actual endpoints for the treatment domain
        retrieved_context = "No endpoints found."
        try:
            connector = PubMedConnector(max_results=2)
            # Find a proxy term from methodology (e.g. treatment arms)
            arms = methodology.treatment_arms if hasattr(methodology, "treatment_arms") else methodology.get("treatment_arms", [])
            query = "clinical trial endpoints " + " ".join(arms)
            entries = connector.fetch_literature_provenance(query)
            if entries:
                retrieved_context = "\n".join([e.claim_text for e in entries])
        except Exception:
            pass

        
        context = {
            "methodology": str(methodology),
            "retrieved_clinical_endpoints": retrieved_context,
            "controls": "None",
            "failure_criteria": "None"
        }

        spec = TaskSpecification(
            task_type=CognitiveTaskType.STATISTICAL_POWER_ANALYSIS, # Reusing
            context=context,
            expected_schema=schema_hint,
            strict_falsifiability=True,
        )
        
        spec.context["INSTRUCTION"] = "Analyze safety and efficacy endpoints using the provided retrieved_clinical_endpoints to ground your choice of primary endpoints rather than hallucinating them."

        return self.planner.execute_task(spec)


class ClinicalProtocolGenerator:
    def __init__(self, planner: ReasoningPlanner | None) -> None:
        self.planner = planner

    def generate(self, methodology: dict[str, Any], cohort: dict[str, Any], safety: dict[str, Any]) -> dict[str, Any]:
        if not self.planner:
            return {"protocol_steps": []}

        schema_hint = ExecutionProtocolModel

        context = {
            "methodology": str(methodology),
            "cohort": str(cohort),
            "safety": str(safety),
            "statistical_design": str(safety)
        }

        spec = TaskSpecification(
            task_type=CognitiveTaskType.EXECUTION_PROTOCOL_GENERATION,
            context=context,
            expected_schema=schema_hint,
            strict_falsifiability=True,
        )

        spec.context["INSTRUCTION"] = "Generate a clinical trial protocol."

        return self.planner.execute_task(spec)


class ClinicalTrialPlanner(BaseDomainPlanner):
    """
    A specialized planner for clinical trial design.
    Removes wet-lab constraints and implements clinical trial specific reasoning.
    """

    def __init__(self, gateway: IntelligenceGateway | None = None, ablation_config: AblationConfig | None = None) -> None:
        self.ablation_config = ablation_config or AblationConfig()
        self.planner = ReasoningPlanner(gateway) if gateway else None
        
        self.methodology_generator = ClinicalMethodologyGenerator(self.planner)
        self.cohort_validator = CohortSelectionValidator(self.planner)
        self.safety_analyzer = SafetyAndEfficacyAnalyzer(self.planner)
        self.protocol_generator = ClinicalProtocolGenerator(self.planner)

    def design_experiment(
        self, hypothesis: dict[str, Any], ledger_entry: dict[str, Any] | None, knowledge_context: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Executes the modules sequentially and constructs the clinical trial design payload.
        """
        if not ledger_entry:
            raise ValueError(
                "Hypothesis lacks provenance. A ledger_entry is required to enter experimental planning."
            )

        readiness = ledger_entry.get("readiness")
        if readiness not in ["readyForCausal", "readyForExperiment"]:
            raise ValueError(
                f"Hypothesis failed M9.25 governance gate. Readiness level '{readiness}' is insufficient for experimental planning."
            )

        # Stage 1: Methodology
        methodology = self.methodology_generator.generate(hypothesis, self.ablation_config)

        # Stage 2: Cohort Selection
        cohort = self.cohort_validator.validate(hypothesis.get("claim", ""), methodology)
        
        # Stage 3: Safety & Efficacy
        safety = self.safety_analyzer.analyze(methodology)

        # Stage 4: Protocol
        protocol = self.protocol_generator.generate(methodology, cohort, safety)

        return {
            "id": f"exp-{uuid.uuid4()}",
            "hypothesisId": hypothesis.get("id", "unknown_hyp"),
            "domain": "CLINICAL_TRIAL",
            "treatment_arms": getattr(methodology, "treatment_arms", methodology.get("treatment_arms", []) if isinstance(methodology, dict) else []),
            "comparator_arms": getattr(methodology, "comparator_arms", methodology.get("comparator_arms", []) if isinstance(methodology, dict) else []),
            "blinding_strategy": getattr(methodology, "blinding_strategy", methodology.get("blinding_strategy", "") if isinstance(methodology, dict) else ""),
            "randomization": getattr(methodology, "randomization", methodology.get("randomization", "") if isinstance(methodology, dict) else ""),
            "successCriteria": getattr(methodology, "success_criteria", methodology.get("success_criteria", "") if isinstance(methodology, dict) else ""),
            "inclusion_criteria": getattr(cohort, "inclusion_criteria", cohort.get("inclusion_criteria", []) if isinstance(cohort, dict) else []),
            "exclusion_criteria": getattr(cohort, "exclusion_criteria", cohort.get("exclusion_criteria", []) if isinstance(cohort, dict) else []),
            "primary_endpoints": getattr(safety, "primary_endpoints", safety.get("primary_endpoints", []) if isinstance(safety, dict) else []),
            "secondary_endpoints": getattr(safety, "secondary_endpoints", safety.get("secondary_endpoints", []) if isinstance(safety, dict) else []),
            "safety_monitoring_plan": getattr(safety, "safety_monitoring_plan", safety.get("safety_monitoring_plan", "") if isinstance(safety, dict) else ""),
            "protocol_steps": getattr(protocol, "protocol_steps", protocol.get("protocol_steps", []) if isinstance(protocol, dict) else []),
            "assumptions": getattr(protocol, "assumptions", protocol.get("assumptions", []) if isinstance(protocol, dict) else []),
            "sampleSize": {"n_per_group": 100, "justification": "Mock size for verification."},
            "controls": [{"group_name": "placebo", "purpose_and_justification": "Mock control for verification."}]
        }
