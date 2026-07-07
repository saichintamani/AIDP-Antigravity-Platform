from typing import Any

from aidp.intelligence.prompts.registry import PromptRegistry
from aidp.intelligence.providers.capabilities import ReasoningTier
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.task_specification import CognitiveTaskType, TaskSpecification


class ReasoningPlanner:
    """
    Consumes a TaskSpecification, selects the appropriate prompt templates and capabilities,
    and drives execution through the IntelligenceGateway.
    """

    def __init__(self, gateway: IntelligenceGateway) -> None:
        self.gateway = gateway

    def execute_task(self, spec: TaskSpecification) -> Any:
        prompt_template = self._map_task_to_prompt(spec.task_type, spec.context)
        min_tier = self._map_task_to_tier(spec.task_type)

        # Render the prompt
        pt = PromptRegistry.get(prompt_template)
        prompt_str = pt.render(spec.context)

        return self.gateway.query(
            prompt=prompt_str,
            schema_hint=spec.expected_schema,
            prompt_version=pt.version_hash,
            min_tier=min_tier,
        )

    def _map_task_to_prompt(self, task_type: CognitiveTaskType, context: dict[str, Any]) -> str:
        if task_type == CognitiveTaskType.HYPOTHESIS_GENERATION:
            return "hypothesis_generator"
        elif task_type == CognitiveTaskType.EXPERIMENT_PLANNING:
            return "experiment_planner"
        elif task_type == CognitiveTaskType.STATISTICIAN_REVIEW:
            return "statistician_review"
        elif task_type == CognitiveTaskType.DOMAIN_REVIEW:
            return "domain_expert_review"
        elif task_type == CognitiveTaskType.METHODOLOGY_REVIEW:
            return "methodologist_review"
        elif task_type == CognitiveTaskType.ENGINEERING_REVIEW:
            return "engineer_review"
        elif task_type == CognitiveTaskType.ETHICS_REVIEW:
            return "ethicist_review"
        else:
            raise ValueError(f"Unsupported task type for mapping: {task_type}")

    def _map_task_to_tier(self, task_type: CognitiveTaskType) -> ReasoningTier:
        if task_type in [
            CognitiveTaskType.HYPOTHESIS_GENERATION,
            CognitiveTaskType.EXPERIMENT_PLANNING,
        ]:
            return ReasoningTier.EXPERT
        elif task_type in [
            CognitiveTaskType.STATISTICIAN_REVIEW,
            CognitiveTaskType.DOMAIN_REVIEW,
            CognitiveTaskType.METHODOLOGY_REVIEW,
            CognitiveTaskType.ENGINEERING_REVIEW,
            CognitiveTaskType.ETHICS_REVIEW,
        ]:
            return ReasoningTier.COMPLEX
        return ReasoningTier.BASIC
