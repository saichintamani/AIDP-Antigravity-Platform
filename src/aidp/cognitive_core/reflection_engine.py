from typing import Optional, Any


class ReflectionEngine:
    """
    Implements a self-improving memory module.
    Records systemic mistakes, successful patterns, provider quality, and reasoning failures.
    """

    def __init__(self) -> None:
        self.ledger: list[dict[str, Any]] = []

    def log_reflection(self, context: str, category: str, observation: str, impact: str) -> None:
        """
        Logs a reflection event.
        Categories: MISTAKE, SUCCESS, PROVIDER_QUALITY, REASONING_FAILURE
        """
        entry = {
            "context": context,
            "category": category,
            "observation": observation,
            "impact": impact,
        }
        self.ledger.append(entry)

    def query_lessons(self, category: Optional[str] = None) -> list[dict[str, Any]]:
        """
        Retrieves past lessons for the planner to consult before executing a new strategy.
        """
        if category:
            return [entry for entry in self.ledger if entry["category"] == category]
        return self.ledger
