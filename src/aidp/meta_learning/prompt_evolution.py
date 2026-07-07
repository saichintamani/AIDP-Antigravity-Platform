

class PromptVariant:
    def __init__(self, id: str, content: str) -> None:
        self.id = id
        self.content = content
        self.times_used = 0
        self.cumulative_discovery_value = 0.0

    @property
    def average_score(self) -> float:
        if self.times_used == 0:
            return 0.0
        return self.cumulative_discovery_value / self.times_used


class PromptRegistry:
    """
    Manages prompt versions and autonomous A/B testing (E2).
    """

    def __init__(self) -> None:
        self.prompts: dict[str, list[PromptVariant]] = {}

    def register_prompt(self, role: str, variant_id: str, content: str) -> None:
        if role not in self.prompts:
            self.prompts[role] = []
        self.prompts[role].append(PromptVariant(variant_id, content))

    def get_best_prompt(self, role: str) -> str:
        """
        Returns the content of the prompt with the highest average DiscoveryValue.
        """
        variants = self.prompts.get(role, [])
        if not variants:
            raise ValueError(f"No prompts registered for role: {role}")

        # If any have 0 uses, we should return them to explore
        for v in variants:
            if v.times_used == 0:
                return v.content

        # Exploit the best performing prompt
        best_variant = max(variants, key=lambda x: x.average_score)
        return best_variant.content

    def log_performance(self, role: str, variant_content: str, discovery_value: float) -> None:
        variants = self.prompts.get(role, [])
        for v in variants:
            if v.content == variant_content:
                v.times_used += 1
                v.cumulative_discovery_value += discovery_value
                break
