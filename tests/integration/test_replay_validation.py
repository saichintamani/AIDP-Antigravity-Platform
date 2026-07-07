import pytest

from aidp.intelligence.providers.middleware import GatewayTrace
from aidp.reasoning.replay import ReasoningReplayEngine


def dummy_reasoner(query: str) -> dict:
    return {"finalDecision": "approved"}


def test_replay_fails_fast_on_missing_metadata() -> None:
    """
    Gate 2: Replay Reproducibility Validation.
    Verifies that the replay engine strictly fails if trace forensics are incomplete.
    """
    engine = ReasoningReplayEngine(dummy_reasoner)

    # Trace missing 'routing_decision'
    bad_trace = GatewayTrace(
        request_id="req-123",
        timestamp="2026-07-06T00:00:00Z",
        provider_name="MockLLM",
        prompt_version="v1.0",
        latency_ms=100.0,
        retries=0,
        cache_hit=False,
        input_tokens=10,
        output_tokens=10,
        estimated_cost_usd=0.0,
        safety_violations=[],
        success=True,
        model_identifier="mock-v1",
        decoding_parameters={},
        routing_decision="",  # Missing this metadata
    )

    historical_trace = {"query": "Should we test this?", "gateway_traces": [bad_trace]}

    with pytest.raises(
        ValueError, match="missing required forensic metadata: \\['routing_decision'\\]"
    ):
        engine.replay_and_compare(historical_trace)


def test_replay_succeeds_with_complete_metadata() -> None:
    engine = ReasoningReplayEngine(dummy_reasoner)

    good_trace = GatewayTrace(
        request_id="req-123",
        timestamp="2026-07-06T00:00:00Z",
        provider_name="MockLLM",
        prompt_version="v1.0",
        latency_ms=100.0,
        retries=0,
        cache_hit=False,
        input_tokens=10,
        output_tokens=10,
        estimated_cost_usd=0.0,
        safety_violations=[],
        success=True,
        model_identifier="mock-v1",
        decoding_parameters={},
        routing_decision="EXPERT",
    )

    historical_trace = {
        "query": "Should we test this?",
        "gateway_traces": [good_trace],
        "finalDecision": "approved",
    }

    score = engine.replay_and_compare(historical_trace)
    assert score == 1.0
