from aidp.meta_learning.discovery_memory import DiscoveryMemory


class ExperienceReplayEngine:
    """
    Samples past failed or successful campaigns to augment prompts as few-shot context.
    """

    def __init__(self, memory: DiscoveryMemory) -> None:
        self.memory = memory

    def generate_context_for_planner(self, domain: str) -> str:
        """
        Retrieves failed campaigns in the same domain so the planner doesn't repeat them.
        """
        failures = self.memory.retrieve_failed_campaigns(domain, max_results=3)
        if not failures:
            return ""

        context = "AVOID REPEATING THESE PAST FAILURES:\n"
        for f in failures:
            context += f"- Goal: {f['goal']} (EIG was {f['eig_score']})\n"

        return context
