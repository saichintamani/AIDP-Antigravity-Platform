from typing import Any

import pytest

from aidp.intelligence.providers.capabilities import LOCAL_MOCK_CAPABILITIES
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.providers.routing import RoutingPolicy


class MalformedJSONProvider:
    model_name = "malformed-mock"
    default_params = {}

    def query(self, prompt: str, schema_hint: dict[str, Any] | None = None) -> Any:
        return "This is not JSON { oops"


class InvalidSchemaProvider:
    model_name = "invalid-schema-mock"
    default_params = {}

    def query(self, prompt: str, schema_hint: dict[str, Any] | None = None) -> Any:
        return '{"wrong_key": 123}'


def test_gateway_graceful_degradation_malformed_json() -> None:
    """Gate 7: Ensure gateway catches and retries JSON parse errors safely."""
    routing = RoutingPolicy()
    routing.register_provider("malformed", MalformedJSONProvider(), LOCAL_MOCK_CAPABILITIES)
    gateway = IntelligenceGateway(routing_policy=routing)

    with pytest.raises(RuntimeError, match="LLM failed validation"):
        gateway.query("prompt", schema_hint={"needed": None})

    # Check trace was recorded
    assert len(gateway.traces) == 1
    trace = gateway.traces[0]
    assert trace.success is False
    assert trace.retries == 2  # Attempted 3 times total (retries 2)


def test_gateway_graceful_degradation_invalid_schema() -> None:
    """Gate 7: Ensure gateway catches schema mismatch."""
    routing = RoutingPolicy()
    routing.register_provider("invalid", InvalidSchemaProvider(), LOCAL_MOCK_CAPABILITIES)
    gateway = IntelligenceGateway(routing_policy=routing)

    with pytest.raises(RuntimeError, match="JSON missing required keys"):
        gateway.query("prompt", schema_hint={"needed": None})

    assert len(gateway.traces) == 1
    assert gateway.traces[0].success is False
