import pytest
from unittest.mock import MagicMock
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.providers.routing import RoutingPolicy
from aidp.intelligence.providers.capabilities import LOCAL_MOCK_CAPABILITIES
import requests

def test_gateway_timeout_degradation():
    """
    Simulates a 504 Gateway Timeout or similar network timeout.
    Verifies that the Gateway raises an expected failure instead of crashing the process.
    """
    routing_policy = RoutingPolicy()
    gateway = IntelligenceGateway(routing_policy=routing_policy)
    
    mock_provider = MagicMock()
    mock_provider.execute_request.side_effect = requests.exceptions.Timeout("Connection timed out")
    mock_provider.query.side_effect = requests.exceptions.Timeout("Connection timed out")
    
    routing_policy.register_provider("mock", mock_provider, LOCAL_MOCK_CAPABILITIES)
    
    # Simulate routing assigning mock
    routing_policy.get_best_provider = MagicMock(return_value=mock_provider)
    
    with pytest.raises(Exception):
        gateway.query("Test prompt")

def test_gateway_rate_limit_handling():
    """
    Simulates a 429 Too Many Requests.
    """
    routing_policy = RoutingPolicy()
    gateway = IntelligenceGateway(routing_policy=routing_policy)
    
    mock_provider = MagicMock()
    mock_provider.query.side_effect = Exception("429 Too Many Requests")
    
    routing_policy.register_provider("mock", mock_provider, LOCAL_MOCK_CAPABILITIES)
    routing_policy.get_best_provider = MagicMock(return_value=mock_provider)
    
    with pytest.raises(Exception):
        gateway.query("Test prompt")

def test_malformed_paper_simulation():
    """
    Simulates ingesting a malformed paper (e.g. empty string).
    The system should parse it gracefully without crashing.
    """
    from aidp.knowledge.extraction.paper_parser import PaperParser
    parser = PaperParser()
    
    # Missing abstract/empty text
    malformed_data = ""
    
    parsed = parser.parse_paper(malformed_data)
    assert "entities" in parsed
    assert "relations" in parsed
