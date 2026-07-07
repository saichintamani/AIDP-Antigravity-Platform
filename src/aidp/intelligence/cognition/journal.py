import time
import uuid
from dataclasses import dataclass, field


@dataclass
class DecisionRecord:
    """
    A permanent, reproducible record of a scientific decision made by an agent.
    """

    agent_id: str
    decision_type: str
    evidence_used: list[str]  # Provenance IDs
    alternatives_rejected: list[str]
    confidence: float
    expected_impact: str
    final_choice: str
    timestamp: float = field(default_factory=time.time)
    id: str = field(default_factory=lambda: f"dec_{uuid.uuid4()}")


class DecisionJournal:
    """
    Append-only ledger of all decisions made by the laboratory staff.
    """

    def __init__(self) -> None:
        self.records: list[DecisionRecord] = []

    def log_decision(self, record: DecisionRecord) -> None:
        self.records.append(record)

    def get_agent_decisions(self, agent_id: str) -> list[DecisionRecord]:
        return [r for r in self.records if r.agent_id == agent_id]


class ReputationSystem:
    """
    Tracks the historical reliability of agents and weights their opinions.
    """

    def __init__(self) -> None:
        # Maps agent_role -> list of (is_correct: bool)
        self.history: dict[str, list[bool]] = {}

    def log_outcome(self, agent_role: str, is_correct: bool) -> None:
        if agent_role not in self.history:
            self.history[agent_role] = []
        self.history[agent_role].append(is_correct)

    def get_reputation_weight(self, agent_role: str) -> float:
        """
        Calculates a weight between 0.1 and 1.0 based on historical accuracy.
        Defaults to 1.0 for new agents.
        """
        outcomes = self.history.get(agent_role, [])
        if not outcomes:
            return 1.0

        accuracy = sum(outcomes) / len(outcomes)

        # Base weight is heavily penalized if accuracy drops below 50%
        return max(0.1, accuracy)
