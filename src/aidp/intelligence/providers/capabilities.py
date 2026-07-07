from dataclasses import dataclass
from enum import Enum


class ReasoningTier(Enum):
    BASIC = 1
    COMPLEX = 2
    EXPERT = 3


@dataclass
class ProviderCapabilities:
    """
    Defines the capabilities of a Foundation Model provider.
    Used by the RoutingPolicy to select the most appropriate model for a given task.
    """

    structured_output: bool
    tool_calling: bool
    streaming: bool
    vision: bool
    max_context: int
    supports_json_schema: bool
    reasoning_tier: ReasoningTier
    cost_per_1m_input_tokens: float
    cost_per_1m_output_tokens: float


# Pre-defined capabilities for standard providers
GEMINI_1_5_PRO_CAPABILITIES = ProviderCapabilities(
    structured_output=True,
    tool_calling=True,
    streaming=True,
    vision=True,
    max_context=2_000_000,
    supports_json_schema=True,
    reasoning_tier=ReasoningTier.EXPERT,
    cost_per_1m_input_tokens=1.25,
    cost_per_1m_output_tokens=5.00,
)

GPT_4O_CAPABILITIES = ProviderCapabilities(
    structured_output=True,
    tool_calling=True,
    streaming=True,
    vision=True,
    max_context=128_000,
    supports_json_schema=True,
    reasoning_tier=ReasoningTier.EXPERT,
    cost_per_1m_input_tokens=5.00,
    cost_per_1m_output_tokens=15.00,
)

CLAUDE_3_5_SONNET_CAPABILITIES = ProviderCapabilities(
    structured_output=True,
    tool_calling=True,
    streaming=True,
    vision=True,
    max_context=200_000,
    supports_json_schema=True,
    reasoning_tier=ReasoningTier.EXPERT,
    cost_per_1m_input_tokens=3.00,
    cost_per_1m_output_tokens=15.00,
)

LOCAL_MOCK_CAPABILITIES = ProviderCapabilities(
    structured_output=True,
    tool_calling=False,
    streaming=False,
    vision=False,
    max_context=4_096,
    supports_json_schema=False,
    reasoning_tier=ReasoningTier.BASIC,
    cost_per_1m_input_tokens=0.0,
    cost_per_1m_output_tokens=0.0,
)
