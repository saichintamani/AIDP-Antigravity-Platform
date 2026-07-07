from aidp.intelligence.providers.capabilities import LOCAL_MOCK_CAPABILITIES
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.providers.mock import MockProvider
from aidp.intelligence.providers.routing import RoutingPolicy


def test_gateway_telemetry_fields() -> None:
    """
    Gate 6: Observability Validation.
    Every gateway invocation must emit structured telemetry answering:
    - Which provider handled the request?
    - Why was that provider selected? (routing_decision)
    - How many retries?
    - Was cached output used?
    """
    routing = RoutingPolicy()
    routing.register_provider("mock", MockProvider(), LOCAL_MOCK_CAPABILITIES)
    gateway = IntelligenceGateway(routing_policy=routing)

    # 1. Fresh call
    gateway.query("prompt 1")
    trace1 = gateway.traces[0]

    assert trace1.provider_name == "MockProvider"
    assert trace1.routing_decision == "BASIC"
    assert trace1.cache_hit is False
    assert trace1.retries == 0
    assert trace1.request_id != ""
    assert trace1.timestamp != ""
    assert trace1.latency_ms >= 0

    # 2. Cached call
    gateway.query("prompt 1")
    trace2 = gateway.traces[1]

    assert trace2.cache_hit is True
    assert "Cached" in trace2.routing_decision
