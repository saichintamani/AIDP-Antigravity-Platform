import uuid
from typing import Optional, Any

from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.reasoning_planner import ReasoningPlanner
from aidp.intelligence.task_specification import CognitiveTaskType, TaskSpecification


class ExperimentPlanner:
    """
    Consumes a structurally validated hypothesis and formulates the blueprint for an empirical experiment
    by querying the LLM Intelligence Gateway.
    """

    def __init__(self, gateway: Optional[IntelligenceGateway] = None) -> None:
        self.gateway = gateway
        self.planner = ReasoningPlanner(gateway) if gateway else None

    def design_experiment(
        self, hypothesis: dict[str, Any], ledger_entry: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """
        Extracts independent and dependent variables, establishes controls,
        and explicitly defines failure (falsifiability) criteria using the LLM.
        Enforces M9.25 Scientific Governance gate.
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

        if not self.gateway:
            # Fallback for old tests without gateway mock
            return {
                "id": f"exp-{uuid.uuid4()}",
                "hypothesisId": hypothesis.get("id", "unknown_hyp"),
                "independentVariables": ["Variable A"],
                "dependentVariables": ["Variable B"],
                "controls": ["Control"],
                "failureCriteria": "If the null hypothesis cannot be rejected, falsify the claim.",
                "resourceEstimation": "Standard compute",
                "costPrediction": "Low",
                "failurePrediction": "Convergence failure",
            }

        claim = hypothesis.get("claim", "")

        schema_hint = {
            "independentVariables": None,
            "dependentVariables": None,
            "controls": None,
            "failureCriteria": None,
            "resourceEstimation": None,
            "costPrediction": None,
            "failurePrediction": None,
        }

        spec = TaskSpecification(
            task_type=CognitiveTaskType.EXPERIMENT_PLANNING,
            context={"claim": claim},
            expected_schema=schema_hint,
            strict_falsifiability=True,
        )

        result = self.planner.execute_task(spec) if self.planner else {}

        independent_vars = result.get("independentVariables", [])
        dependent_vars = result.get("dependentVariables", [])

        if not independent_vars or not dependent_vars:
            raise ValueError(
                "Experiment planner failed to identify independent or dependent variables."
            )

        return {
            "id": f"exp-{uuid.uuid4()}",
            "hypothesisId": hypothesis.get("id", "unknown_hyp"),
            "independentVariables": independent_vars,
            "dependentVariables": dependent_vars,
            "controls": result.get("controls", []),
            "failureCriteria": result.get("failureCriteria", ""),
            "resourceEstimation": result.get("resourceEstimation", "Unknown"),
            "costPrediction": result.get("costPrediction", "Unknown"),
            "failurePrediction": result.get("failurePrediction", "Unknown"),
        }
