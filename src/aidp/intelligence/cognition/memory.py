from typing import Any


class HierarchicalMemory:
    """
    Isolated memory store for an individual agent.
    Maintains partitions for different types of memory.
    """

    def __init__(self) -> None:
        self.working_memory: list[dict[str, Any]] = []
        self.episodic_memory: list[dict[str, Any]] = []
        self.semantic_memory: list[dict[str, Any]] = []
        self.procedural_memory: list[dict[str, Any]] = []
        self.reflection_memory: list[dict[str, Any]] = []

    def add_to_working_memory(self, item: dict[str, Any]) -> None:
        self.working_memory.append(item)

    def archive_to_episodic(self, campaign_id: str) -> None:
        """Moves working memory context to long-term episodic storage."""
        self.episodic_memory.append(
            {"campaign_id": campaign_id, "events": list(self.working_memory)}
        )
        self.working_memory.clear()

    def add_failure_reflection(self, goal: str, mistake: str, correction: str) -> None:
        """Records a failure in the reflection memory to prevent repetition."""
        self.reflection_memory.append({"goal": goal, "mistake": mistake, "correction": correction})

    def add_procedural_rule(self, rule: str, domain: str) -> None:
        self.procedural_memory.append({"rule": rule, "domain": domain})

    def clear_working_memory(self) -> None:
        self.working_memory.clear()
