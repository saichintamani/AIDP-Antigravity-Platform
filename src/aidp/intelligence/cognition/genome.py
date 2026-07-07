import copy
import uuid
from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class ScientistIdentity:
    role: str
    specialization: str
    expertise: dict[str, float] = field(default_factory=dict)
    confidence_calibration: float = 1.0  # 1.0 = perfectly calibrated
    decision_style: str = "balanced"
    risk_tolerance: str = "medium"
    known_weaknesses: list[str] = field(default_factory=list)


@dataclass
class AgentGenome:
    """
    Version-controlled configuration object describing a digital scientist.
    Allows exact cloning, rollback, and reproducibility of any scientific agent.
    """

    identity: ScientistIdentity
    prompt_version: str = "v1.0"
    base_prompt: str = ""
    reasoning_strategies: dict[str, float] = field(
        default_factory=lambda: {"chain_of_thought": 1.0, "tree_of_thought": 0.5}
    )
    performance_history: list[dict[str, Any]] = field(default_factory=list)
    version: int = 1
    id: str = field(default_factory=lambda: f"genome_{uuid.uuid4()}")

    def clone(self) -> "AgentGenome":
        """Creates an exact clone of the current genome."""
        return copy.deepcopy(self)

    def spawn_child_version(self, new_prompt: Optional[str] = None) -> "AgentGenome":
        """Creates a v+1 genome, e.g. for prompt A/B testing."""
        child = self.clone()
        child.version += 1
        child.id = f"genome_{uuid.uuid4()}"
        if new_prompt:
            child.base_prompt = new_prompt
            child.prompt_version = f"v{child.version}.0"
        return child
