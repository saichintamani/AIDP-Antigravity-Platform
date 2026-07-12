from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class CognitiveTaskType(Enum):
    HYPOTHESIS_GENERATION = "HYPOTHESIS_GENERATION"
    EXPERIMENT_PLANNING = "EXPERIMENT_PLANNING"
    EVIDENCE_LINKAGE_VALIDATION = "EVIDENCE_LINKAGE_VALIDATION"
    METHODOLOGY_GENERATION = "METHODOLOGY_GENERATION"
    STATISTICAL_DESIGN_VALIDATION = "STATISTICAL_DESIGN_VALIDATION"
    STATISTICIAN_REVIEW = "STATISTICIAN_REVIEW"
    DOMAIN_REVIEW = "DOMAIN_REVIEW"
    METHODOLOGY_REVIEW = "METHODOLOGY_REVIEW"
    ENGINEERING_REVIEW = "ENGINEERING_REVIEW"
    ETHICS_REVIEW = "ETHICS_REVIEW"
    KNOWLEDGE_EXTRACTION = "KNOWLEDGE_EXTRACTION"
    EPISTEMIC_VALIDATION = "EPISTEMIC_VALIDATION"


@dataclass
class TaskSpecification:
    """
    Decouples the abstract cognitive intent from specific prompt templates or routing decisions.
    """

    task_type: CognitiveTaskType
    context: dict[str, Any]
    expected_schema: dict[str, Any] | None = None
    strict_falsifiability: bool = True
    context_window_hint: int = 4096
    metadata: dict[str, Any] = field(default_factory=dict)
