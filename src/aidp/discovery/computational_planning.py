import uuid
from typing import Any

from aidp.discovery.scientific_planning import AblationConfig, BaseDomainPlanner
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.reasoning_planner import ReasoningPlanner
from aidp.intelligence.task_specification import CognitiveTaskType, TaskSpecification


class ComputationalPlanner(BaseDomainPlanner):
    """
    Synthesizes in silico computational screening / modeling protocols.
    """
    def __init__(self, gateway: IntelligenceGateway) -> None:
        self.gateway = gateway
        self.planner = ReasoningPlanner(gateway)
        self.ablation_config = AblationConfig()

    def design_experiment(
        self, hypothesis: dict[str, Any], ledger_entry: dict[str, Any] | None, knowledge_context: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Orchestrates the LLM tasks to build a computational protocol.
        """
        claim = hypothesis.get("claim", "")
        
        # 1. Hardware & Algorithm Specs
        spec_hardware = TaskSpecification(
            task_type=CognitiveTaskType.METHODOLOGY_GENERATION,
            context={"claim": claim, "domain": "Computational", "evidence_mapping": "{}"},
            expected_schema={
                "algorithm": "string",
                "hardware_requirements": "string",
                "software_dependencies": "list[string]"
            }
        )
        hardware_res = self.planner.execute_task(spec_hardware)
        if not hardware_res:
            hardware_res = {
                "algorithm": "Molecular Dynamics (GROMACS)",
                "hardware_requirements": "8x A100 GPUs",
                "software_dependencies": ["gromacs", "openff"]
            }

        # 2. Dataset Split
        spec_data = TaskSpecification(
            task_type=CognitiveTaskType.METHODOLOGY_GENERATION,
            context={"claim": claim, "domain": "Computational", "evidence_mapping": "{}"},
            expected_schema={
                "training_set": "string",
                "validation_set": "string",
                "test_set": "string",
                "cross_validation_folds": "integer"
            }
        )
        data_res = self.planner.execute_task(spec_data)
        if not data_res:
            data_res = {
                "training_set": "ZINC20 Database",
                "validation_set": "Holdout subset (10%)",
                "test_set": "External benchmark dataset",
                "cross_validation_folds": 5
            }

        return {
            "protocol_id": f"comp_{uuid.uuid4()}",
            "domain": "COMPUTATIONAL",
            "methodology": {
                "hardware": hardware_res,
                "data_splits": data_res
            },
            "status": "DRAFT",
            "assumptions": ["Force fields accurately model biological environment", "GPU clusters remain available"]
        }
