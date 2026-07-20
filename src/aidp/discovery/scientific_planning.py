import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from aidp.intelligence.models import (
    ControlTaxonomy,
    EngineerFeasibility,
    EvidenceLinkage,
    ExecutionProtocolModel,
    Methodology,
)
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.reasoning_planner import ReasoningPlanner
from aidp.intelligence.task_specification import CognitiveTaskType, TaskSpecification


@dataclass
class AblationConfig:
    enable_spl: bool = True
    enable_schema_sync: bool = True
    enable_falsifiability: bool = True
    enable_power_analyzer: bool = True

def _get_val(obj, key, default=""):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)

def _dump_obj(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if isinstance(obj, list):
        return [_dump_obj(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _dump_obj(v) for k, v in obj.items()}
    return obj

class BaseDomainPlanner(ABC):
    @abstractmethod
    def design_experiment(
        self, hypothesis: dict[str, Any], ledger_entry: dict[str, Any] | None, knowledge_context: dict[str, Any]
    ) -> dict[str, Any]:
        pass


class EvidenceLinkageValidator:
    def __init__(self, planner: ReasoningPlanner | None) -> None:
        self.planner = planner

    def validate(self, hypothesis: dict[str, Any], knowledge_context: dict[str, Any]) -> dict[str, Any]:
        if not self.planner:
            return {
                "evidence_to_claim_mapping": [{"claim_component": "Mock Claim", "supporting_evidence": "Mock Evidence"}],
                "supporting_dois": ["10.mock/123"],
                "unsupported_claims": [],
                "evidence_confidence": "High"
            }

        claim = hypothesis.get("claim", "")
        rationale = hypothesis.get("rationale", "")
        documents = knowledge_context.get("documents", [])
        evidence_str = "\n".join([f"DOI: {doc.get('source_doi')} - {doc.get('text')}" for doc in documents])

        schema_hint = EvidenceLinkage

        spec = TaskSpecification(
            task_type=CognitiveTaskType.EVIDENCE_LINKAGE_VALIDATION,
            context={"claim": claim, "rationale": rationale, "evidence": evidence_str},
            expected_schema=schema_hint,
            strict_falsifiability=True,
        )

        return self.planner.execute_task(spec)


class ExperimentalMethodologyGenerator:
    def __init__(self, planner: ReasoningPlanner | None) -> None:
        self.planner = planner

    def generate(self, hypothesis: dict[str, Any], evidence_linkage: dict[str, Any], ablation_config: AblationConfig | None = None) -> dict[str, Any]:
        if not self.planner:
            return {
                "independent_variables": ["Mock IV"],
                "dependent_variables": ["Mock DV"],
                "control_groups": [{"group_name": "Mock Control", "purpose": "Baseline"}],
                "confounders_identified": ["Mock Confounder"],
                "success_criteria": "Mock Success Criteria"
            }

        claim = hypothesis.get("claim", "")
        
        # Inject Failure Memory
        from aidp.memory.failure_memory import FailureMemoryManager
        fm = FailureMemoryManager()
        recent_failures = fm.get_failures(domain="WetLab", limit=3)
        failure_context = ""
        if recent_failures:
            failure_context = "AVOID PREVIOUS FAILURES:\n"
            for f in recent_failures:
                failure_context += f"- {f.get('critique')}\n"
        
        schema_hint = Methodology

        if ablation_config and not ablation_config.enable_schema_sync:
            schema_hint = None

        spec = TaskSpecification(
            task_type=CognitiveTaskType.METHODOLOGY_GENERATION,
            context={"claim": claim, "evidence_mapping": str(evidence_linkage), "failure_memory": failure_context},
            expected_schema=schema_hint,
            strict_falsifiability=True,
        )

        return self.planner.execute_task(spec)


class StatisticalPowerAnalyzer:
    def __init__(self, planner: ReasoningPlanner | None) -> None:
        self.planner = planner

    def validate(self, methodology: dict[str, Any], controls: list[dict[str, Any]], failure_criteria: str) -> dict[str, Any]:
        from aidp.verification.statistical_solver import StatisticalSolver
        solver = StatisticalSolver()
        return solver.validate(methodology, failure_criteria)


class FalsifiabilityValidator:
    def __init__(self, planner: ReasoningPlanner | None) -> None:
        self.planner = planner

    def validate(self, hypothesis_claim: str, success_criteria: str, variables: dict[str, Any]) -> dict[str, Any]:
        from aidp.verification.logic_solver import LogicSolver
        solver = LogicSolver()
        return solver.validate(hypothesis_claim, success_criteria, variables)


class ControlTaxonomyGenerator:
    def __init__(self, planner: ReasoningPlanner | None) -> None:
        self.planner = planner

    def generate(self, variables: dict[str, Any], confounders: list[str], ablation_config: AblationConfig | None = None) -> dict[str, Any]:
        if not self.planner:
            return {"controls": [{"group_name": "Mock Control", "purpose": "Baseline"}]}

        schema_hint = ControlTaxonomy

        context = {
            "variables": str(variables),
            "confounders": str(confounders)
        }

        if ablation_config and not ablation_config.enable_schema_sync:
            schema_hint = None

        spec = TaskSpecification(
            task_type=CognitiveTaskType.CONTROL_TAXONOMY_GENERATION,
            context=context,
            expected_schema=schema_hint,
            strict_falsifiability=True,
        )

        return self.planner.execute_task(spec)


class EngineerFeasibilityGenerator:
    def __init__(self, planner: ReasoningPlanner | None) -> None:
        self.planner = planner

    def generate(self, methodology: dict[str, Any]) -> dict[str, Any]:
        if not self.planner:
            return {
                "resource_estimation": "Mock resource estimation",
                "cost_prediction": "Mock cost prediction",
                "failure_prediction": "Mock failure prediction",
                "critical_engineering_risks": []
            }

        schema_hint = EngineerFeasibility

        spec = TaskSpecification(
            task_type=CognitiveTaskType.ENGINEER_FEASIBILITY_GENERATION,
            context={"methodology": str(methodology)},
            expected_schema=schema_hint,
            strict_falsifiability=True,
        )

        return self.planner.execute_task(spec)


class ExecutionProtocolGenerator:
    def __init__(self, planner: ReasoningPlanner | None) -> None:
        self.planner = planner

    def generate(self, methodology: dict[str, Any], statistical_design: dict[str, Any]) -> dict[str, Any]:
        if not self.planner:
            return {"protocol_steps": []}

        schema_hint = ExecutionProtocolModel

        context = {
            "methodology": str(methodology),
            "statistical_design": str(statistical_design)
        }

        spec = TaskSpecification(
            task_type=CognitiveTaskType.EXECUTION_PROTOCOL_GENERATION,
            context=context,
            expected_schema=schema_hint,
            strict_falsifiability=True,
        )

        return self.planner.execute_task(spec)


class WetLabPlanner(BaseDomainPlanner):
    """
    Replaces the single-shot ExperimentPlanner with a sequential validated pipeline.
    """

    def __init__(self, gateway: IntelligenceGateway | None = None, ablation_config: AblationConfig | None = None) -> None:
        self.ablation_config = ablation_config or AblationConfig()
        self.planner = ReasoningPlanner(gateway) if gateway else None
        
        self.evidence_validator = EvidenceLinkageValidator(self.planner)
        self.methodology_generator = ExperimentalMethodologyGenerator(self.planner)
        self.control_taxonomy_generator = ControlTaxonomyGenerator(self.planner)
        self.falsifiability_validator = FalsifiabilityValidator(self.planner)
        self.statistical_power_analyzer = StatisticalPowerAnalyzer(self.planner)

        self.engineer_feasibility_generator = EngineerFeasibilityGenerator(self.planner)
        self.execution_protocol_generator = ExecutionProtocolGenerator(self.planner)

    def design_experiment(
        self, hypothesis: dict[str, Any], ledger_entry: dict[str, Any] | None, knowledge_context: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Executes the modules sequentially and constructs the enriched experimental design payload.
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

        # Stage 1: Evidence Linkage
        evidence_linkage = self.evidence_validator.validate(hypothesis, knowledge_context)
        
        # Stage 2: Methodology
        methodology = self.methodology_generator.generate(hypothesis, evidence_linkage, self.ablation_config)

        # Stage 3: Control Taxonomy
        if isinstance(methodology, dict):
            variables = {
                "independent": methodology.get("independent_variables", []),
                "dependent": methodology.get("dependent_variables", [])
            }
        else:
            variables = {"independent": [], "dependent": []}
            
        control_taxonomy = self.control_taxonomy_generator.generate(
            variables, methodology.get("confounders_identified", []) if isinstance(methodology, dict) else [],
            self.ablation_config
        )
        if isinstance(methodology, dict):
            methodology["control_groups"] = control_taxonomy.get("controls", []) if isinstance(control_taxonomy, dict) else control_taxonomy
        else:
            methodology = {"raw_methodology": methodology, "control_groups": control_taxonomy.get("controls", []) if isinstance(control_taxonomy, dict) else control_taxonomy}

        # Stage 4: Falsifiability
        if self.ablation_config.enable_falsifiability:
            falsifiability = self.falsifiability_validator.validate(
                hypothesis.get("claim", ""),
                methodology.get("success_criteria", ""),
                variables
            )
        else:
            falsifiability = {"failure_criteria": "Ablated", "falsifiability_justification": "Ablated"}

        # Stage 5: Statistical Power Analysis
        if self.ablation_config.enable_power_analyzer:
            stats_design = self.statistical_power_analyzer.validate(
                methodology,
                methodology.get("control_groups", []),
                falsifiability.get("failure_criteria", "")
            )
        else:
            stats_design = {
                "sample_size_recommendation": {"n_per_group": 0, "effect_size": "Ablated", "significance_level_alpha": 0.05, "target_power": 0.8, "justification": "Ablated"},
                "control_isolation_validation": "Ablated",
                "statistical_test": "Ablated",
                "falsifiability_consistency_check": "Ablated"
            }

        # Stage 6: Engineer Feasibility
        engineer_feasibility = self.engineer_feasibility_generator.generate(methodology)

        # Stage 7: Execution Protocol
        execution_protocol = self.execution_protocol_generator.generate(methodology, stats_design)

        raw_method = methodology.get("raw_methodology", methodology) if isinstance(methodology, dict) else methodology

        return _dump_obj({
            "id": f"exp-{uuid.uuid4()}",
            "hypothesisId": hypothesis.get("id", "unknown_hyp"),
            "evidence_to_claim_mapping": _get_val(evidence_linkage, "evidence_to_claim_mapping", []),
            "supporting_dois": _get_val(evidence_linkage, "supporting_dois", []),
            "unsupported_claims": _get_val(evidence_linkage, "unsupported_claims", []),
            "evidence_confidence": _get_val(evidence_linkage, "evidence_confidence", "Unknown"),
            "independentVariables": _get_val(raw_method, "independent_variables", []),
            "dependentVariables": _get_val(raw_method, "dependent_variables", []),
            "controls": [c.get("group_name", "") if isinstance(c, dict) else getattr(c, "group_name", "") for c in _get_val(methodology, "control_groups", [])] if isinstance(_get_val(methodology, "control_groups", []), list) else [c.get("group_name", "") if isinstance(c, dict) else getattr(c, "group_name", "") for c in getattr(_get_val(methodology, "control_groups", []), "controls", [])],
            "confounders": _get_val(raw_method, "confounders_identified", []),
            "successCriteria": _get_val(raw_method, "success_criteria", ""),
            "sampleSize": _get_val(stats_design, "sample_size_recommendation", {}),
            "statisticalTest": _get_val(stats_design, "statistical_test", ""),
            "powerConsiderations": str(_get_val(stats_design, "control_isolation_validation", "")) + "\n" + str(_get_val(stats_design, "falsifiability_consistency_check", "")),
            "reproducibilityNotes": "N/A",
            "failureCriteria": _get_val(falsifiability, "failure_criteria", ""),
            "falsifiabilityJustification": _get_val(falsifiability, "falsifiability_justification", ""),
            "resourceEstimation": _get_val(engineer_feasibility, "resource_estimation", ""),
            "costPrediction": _get_val(engineer_feasibility, "cost_prediction", ""),
            "failurePrediction": _get_val(engineer_feasibility, "failure_prediction", ""),
            "criticalEngineeringRisks": _get_val(engineer_feasibility, "critical_engineering_risks", []),
            "protocol_steps": _get_val(execution_protocol, "protocol_steps", []),
            "assumptions": _get_val(execution_protocol, "assumptions", [])
        })
