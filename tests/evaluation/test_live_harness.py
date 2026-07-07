from aidp.evaluation.live_harness import LiveEvaluationHarness
from aidp.intelligence.providers.base import BaseProvider
from aidp.intelligence.providers.capabilities import ProviderCapabilities, ReasoningTier
from aidp.intelligence.providers.routing import RoutingPolicy


class DummyProvider(BaseProvider):
    def generate(self, prompt: str) -> None:
        pass

    def query(self, prompt: str, schema_hint=None) -> None:
        pass


def test_live_harness_tracking() -> None:
    harness = LiveEvaluationHarness()

    # 12 calls, 12 contradictions (100% rate)
    for _ in range(12):
        harness.log_interaction(
            "gpt-4-turbo", "hypothesis_generation", True, {"has_contradictions": True}
        )

    scorecard = harness.get_scorecard()
    assert scorecard["gpt-4-turbo"]["total_calls"] == 12
    assert scorecard["gpt-4-turbo"]["contradiction_rate"] > 0.9


def test_adaptive_routing_penalty() -> None:
    harness = LiveEvaluationHarness()
    policy = RoutingPolicy(harness=harness)

    # Register two identical capability providers, but A is cheaper
    caps_a = ProviderCapabilities(
        structured_output=True,
        tool_calling=True,
        streaming=True,
        vision=True,
        max_context=1000,
        supports_json_schema=True,
        reasoning_tier=ReasoningTier.EXPERT,
        cost_per_1m_input_tokens=1.0,
        cost_per_1m_output_tokens=1.0,
    )  # $2 total

    caps_b = ProviderCapabilities(
        structured_output=True,
        tool_calling=True,
        streaming=True,
        vision=True,
        max_context=1000,
        supports_json_schema=True,
        reasoning_tier=ReasoningTier.EXPERT,
        cost_per_1m_input_tokens=2.0,
        cost_per_1m_output_tokens=2.0,
    )  # $4 total

    provider_a = DummyProvider()
    provider_b = DummyProvider()

    policy.register_provider("provider_a", provider_a, caps_a)
    policy.register_provider("provider_b", provider_b, caps_b)

    # Without history, provider_a (cheaper) should win
    best = policy.get_best_provider()
    assert best is provider_a

    # Simulate terrible history for provider_a (>10 calls to be statistically significant)
    for _ in range(15):
        harness.log_interaction(
            "provider_a", "hypothesis_generation", True, {"has_contradictions": True}
        )

    # Now provider_b should win because provider_a has a massive penalty
    best = policy.get_best_provider()
    assert best is provider_b
