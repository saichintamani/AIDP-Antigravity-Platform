import time
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ScientificMessage:
    """
    The strictly typed communication protocol for the Autonomous Scientific Laboratory.
    Ensures no raw strings are passed between agents without epistemic context.
    """

    sender: str
    receiver: str
    goal: str
    required_action: str

    # Payload of the message
    payload: dict[str, Any]

    # Epistemic framing
    evidence_ids: list[str] = field(default_factory=list)
    confidence: float = 0.5
    uncertainty: float = 0.5

    # Networking/Tracing
    id: str = field(default_factory=lambda: f"msg_{uuid.uuid4()}")
    timestamp: float = field(default_factory=time.time)

    def validate(self) -> None:
        if not self.sender or not self.receiver:
            raise ValueError("Message must have a sender and receiver.")
        if not self.goal or not self.required_action:
            raise ValueError("Message must define a goal and required_action.")
        if self.confidence < 0.0 or self.confidence > 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0.")
        if self.uncertainty < 0.0 or self.uncertainty > 1.0:
            raise ValueError("Uncertainty must be between 0.0 and 1.0.")
