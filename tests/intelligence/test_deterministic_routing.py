from aidp.intelligence.providers.capabilities import ProviderCapabilities, ReasoningTier
from aidp.intelligence.providers.mock import MockProvider
from aidp.intelligence.providers.routing import RoutingPolicy


def test_deterministic_routing() -> None:
    """
    Gate 4 Validation: Routing must be completely deterministic given
    the same capabilities and constraints.
    """
    routing = RoutingPolicy()

    # Provider A: Basic only
    provider_a = MockProvider()
    routing.register_provider(
        "prov_a",
        provider_a,
        ProviderCapabilities(
            structured_output=True,
            tool_calling=False,
            streaming=False,
            vision=False,
            max_context=1000,
            supports_json_schema=True,
            reasoning_tier=ReasoningTier.BASIC,
            cost_per_1m_input_tokens=1.0,
            cost_per_1m_output_tokens=1.0,
        ),
    )

    # Provider B: Expert
    provider_b = MockProvider()
    routing.register_provider(
        "prov_b",
        provider_b,
        ProviderCapabilities(
            structured_output=True,
            tool_calling=False,
            streaming=False,
            vision=False,
            max_context=1000,
            supports_json_schema=True,
            reasoning_tier=ReasoningTier.EXPERT,
            cost_per_1m_input_tokens=10.0,
            cost_per_1m_output_tokens=10.0,
        ),
    )

    # Run multiple times to verify no randomness/state drift
    for _ in range(5):
        # A request needing EXPERT must deterministically go to prov_b
        res_expert = routing.get_best_provider(min_reasoning_tier=ReasoningTier.EXPERT)
        assert res_expert is provider_b

        # A request needing BASIC could go to either, but we enforce cost-based deterministic routing.
        # Since prov_a costs less (1.0 vs 10.0), it MUST consistently route to prov_a.
        res_basic = routing.get_best_provider(min_reasoning_tier=ReasoningTier.BASIC)
        assert res_basic is provider_a
