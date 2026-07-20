from aidp.intelligence.providers.capabilities import ProviderCapabilities, ReasoningTier, LOCAL_MOCK_CAPABILITIES
from aidp.intelligence.providers.llm import LLMProvider
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.providers.routing import RoutingPolicy

def create_default_gateway() -> IntelligenceGateway:
    provider = LLMProvider()
    caps = LOCAL_MOCK_CAPABILITIES
    policy = RoutingPolicy()
    policy.register_provider("default", provider, caps)
    return IntelligenceGateway(policy)
