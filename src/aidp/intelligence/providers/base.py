from abc import ABC, abstractmethod
from dataclasses import dataclass

from aidp.reasoning.subjective_logic import Opinion


class ProviderError(Exception):
    """Base exception for provider errors."""

    pass


class RateLimitError(ProviderError):
    """Exception for 429 Too Many Requests."""

    pass


@dataclass
class TokenUsage:
    input_tokens: int
    output_tokens: int
    total_cost_usd: float


@dataclass
class NormalizedResponse:
    opinion: Opinion
    usage: TokenUsage
    raw_response: str


class BaseProvider(ABC):
    """
    The provider-agnostic interface for Foundation Models.
    Ensures standard retry, normalization, and token accounting across all vendors.
    """

    @abstractmethod
    def generate(self, prompt: str) -> NormalizedResponse:
        """Generates a structured response based on the provider's specific API."""
        pass
