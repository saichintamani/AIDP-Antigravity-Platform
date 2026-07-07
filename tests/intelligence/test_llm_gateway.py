from typing import Optional, Any

from aidp.intelligence.providers.base import RateLimitError
from aidp.intelligence.providers.capabilities import LOCAL_MOCK_CAPABILITIES
from aidp.intelligence.providers.llm import LLMProvider
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.providers.routing import RoutingPolicy


class FlakyMockProvider:
    def __init__(self) -> None:
        self.call_count = 0

    def query(self, prompt: str, schema_hint: Optional[dict[str, Any]] = None):
        self.call_count += 1

        # 1st call: Rate limit error
        if self.call_count == 1:
            raise RateLimitError("Rate limit exceeded")

        # 2nd call: Malformed JSON (missing a quote)
        if self.call_count == 2:
            return '```json\n{ "hypotheses": [ {"id": "h1", "claim": "Flaky"} \n```'

        # 3rd call: Invalid schema (missing required top-level key "metadata")
        if self.call_count == 3:
            return '```json\n{ "hypotheses": [ {"id": "h1", "claim": "Flaky"} ] }\n```'

        # 4th call: Perfect JSON matching schema
        return '```json\n{ "hypotheses": [ {"id": "h1", "claim": "Fixed", "confidence": 0.9} ], "metadata": "ok" }\n```'


def test_gateway_resilience_and_caching() -> None:
    flaky_provider = FlakyMockProvider()
    routing = RoutingPolicy()
    routing.register_provider("mock", flaky_provider, LOCAL_MOCK_CAPABILITIES)
    gateway = IntelligenceGateway(routing_policy=routing)

    schema_hint = {"hypotheses": None, "metadata": None}

    # 1. Gateway should handle rate limit, retry, hit malformed json, retry with correction,
    # hit invalid schema, retry with correction, and finally succeed on the 4th attempt.
    # But wait, max_validation_retries is 2. Let's see:
    # call 1: RateLimitError -> retried by @with_retry (transparent to query method logic).
    # Inside query loop attempt 0: call 2 -> malformed JSON -> throws ValueError -> caught, loops to attempt 1.
    # Inside query loop attempt 1: call 3 -> missing key -> throws ValueError -> caught, loops to attempt 2.
    # Inside query loop attempt 2: call 4 -> success!

    result = gateway.query("Generate hypotheses.", schema_hint=schema_hint)

    assert result["hypotheses"][0]["claim"] == "Fixed"
    assert len(gateway.traces) == 1
    assert gateway.traces[0].retries == 2
    assert gateway.traces[0].cache_hit is False

    # 2. Test Semantic Caching
    # Should instantly return without hitting provider
    cached_result = gateway.query("Generate hypotheses.", schema_hint=schema_hint)
    assert cached_result["hypotheses"][0]["claim"] == "Fixed"
    assert len(gateway.traces) == 2
    assert gateway.traces[1].cache_hit is True
    assert flaky_provider.call_count == 4  # Has not increased


def test_gateway_with_standard_llm_mock() -> None:
    provider = LLMProvider()
    routing = RoutingPolicy()
    routing.register_provider("mock", provider, LOCAL_MOCK_CAPABILITIES)
    gateway = IntelligenceGateway(routing_policy=routing)

    result = gateway.query("Generate hypotheses.", schema_hint={"hypotheses": None})
    assert len(result["hypotheses"]) == 1
    assert len(gateway.traces) == 1
    assert gateway.traces[0].retries == 0
