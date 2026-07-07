import uuid
from dataclasses import dataclass, field


@dataclass
class ReasoningEvent:
    event_type: str  # e.g., "debate", "hypothesis_generation", "experiment"
    pre_confidence: float
    post_confidence: float
    cost_usd: float
    target_entity: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


class MetaReasoner:
    """
    Evaluates the systemic performance of AIDP components.
    Asks: Was this debate useful? Was the experiment cost-effective?
    """

    def __init__(self) -> None:
        self.events: list[ReasoningEvent] = []

    def log_event(self, event: ReasoningEvent) -> None:
        self.events.append(event)

    def evaluate_debate_efficacy(self) -> float:
        """
        Calculates the average confidence delta produced by debates.
        If a debate doesn't move confidence, it's not useful.
        """
        debate_events = [e for e in self.events if e.event_type == "debate"]
        if not debate_events:
            return 0.0

        total_delta = sum(abs(e.post_confidence - e.pre_confidence) for e in debate_events)
        return total_delta / len(debate_events)

    def evaluate_cost_efficiency(self) -> float:
        """
        Calculates the average confidence gain per dollar spent.
        """
        if not self.events:
            return 0.0

        total_delta = sum(abs(e.post_confidence - e.pre_confidence) for e in self.events)
        total_cost = sum(e.cost_usd for e in self.events)

        if total_cost == 0:
            return float("inf")

        return total_delta / total_cost
