from typing import Any


class ProceduralMemory:
    """Mock storage for learning updates."""

    def __init__(self) -> None:
        self.rules: list[str] = []

    def add_rule(self, rule: str) -> None:
        self.rules.append(rule)


class LearningLoop:
    """
    Extracts patterns from evaluated ReasonTraces (especially weaknesses/failures)
    and commits them to procedural memory.
    """

    def __init__(self, procedural_memory: ProceduralMemory) -> None:
        self.memory = procedural_memory

    def process_trace(self, evaluated_trace: dict[str, Any], scorecard: dict[str, Any]) -> bool:
        """
        If a trace failed evaluation, extracts a rule to prevent future failures.
        Returns True if a rule was generated, False otherwise.
        """
        # MOCK IMPLEMENTATION
        # E.g. If Hallucination was detected, add a rule to enforce evidence grounding.

        hallucinated = scorecard.get("hallucination_detected", False)
        if hallucinated:
            new_rule = "ALWAYS verify hypothesis terms exist in evidence texts."
            self.memory.add_rule(new_rule)
            return True

        return False
