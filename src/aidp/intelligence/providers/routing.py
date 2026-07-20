
from aidp.evaluation.live_harness import LiveEvaluationHarness

from .base import BaseProvider
from .capabilities import ProviderCapabilities, ReasoningTier


class RoutingPolicy:
    """
    Dynamically routes tasks to the most suitable Provider based on registered capabilities
    and empirical performance scorecards.
    """

    def __init__(self, harness: LiveEvaluationHarness | None = None) -> None:
        self._providers: dict[str, tuple[BaseProvider, ProviderCapabilities]] = {}
        self.harness = harness

    def register_provider(
        self, name: str, provider: BaseProvider, capabilities: ProviderCapabilities
    ) -> None:
        """Registers an initialized provider and its capabilities."""
        self._providers[name] = (provider, capabilities)

    def get_best_provider(
        self,
        min_reasoning_tier: ReasoningTier = ReasoningTier.BASIC,
        requires_structured_output: bool = False,
        max_cost_per_1m_tokens: float | None = None,
    ) -> BaseProvider:
        """
        Capability Matcher with Empirical Fallback.
        Selects the cheapest provider that meets the minimum required capabilities,
        but overrides cost if empirical scorecard shows high contradiction rates.
        """
        eligible = []
        for name, (provider, caps) in self._providers.items():
            if caps.reasoning_tier.value < min_reasoning_tier.value:
                continue
            if requires_structured_output and not caps.structured_output:
                continue
            if (
                max_cost_per_1m_tokens
                and (caps.cost_per_1m_input_tokens + caps.cost_per_1m_output_tokens)
                > max_cost_per_1m_tokens
            ):
                continue

            # Apply empirical penalties
            penalty = 0.0
            if self.harness:
                scores = self.harness.get_scorecard().get(name, {})
                if scores.get("total_calls", 0) > 10:  # Statistically significant
                    contradiction_rate = scores.get("contradiction_rate", 0.0)
                    penalty = contradiction_rate * 100.0  # heavy penalty for logic errors

            eligible.append((name, provider, caps, penalty))

        if not eligible:
            raise ValueError(
                f"No registered providers match the requested capabilities. Registered: {list(self._providers.keys())}"
            )

        # Sort by (Total Cost + Empirical Penalty)
        eligible.sort(
            key=lambda x: (x[2].cost_per_1m_input_tokens + x[2].cost_per_1m_output_tokens) + x[3]
        )

        # Return the provider instance of the best match
        return eligible[0][1]
