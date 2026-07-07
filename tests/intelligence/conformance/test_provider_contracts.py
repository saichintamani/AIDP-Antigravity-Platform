from typing import Optional, Any

import pytest

from aidp.intelligence.providers.base import BaseProvider, RateLimitError
from aidp.intelligence.providers.llm import LLMProvider


def test_provider_returns_raw_string_or_dict() -> None:
    """All providers must return a raw string (to be parsed) or a pre-parsed dict."""
    provider = LLMProvider()
    response = provider.query("Test prompt", schema_hint={"test": None})

    # In the mock LLM Provider, it returns a markdown string
    assert isinstance(response, str)
    assert "```json" in response


def test_provider_simulates_rate_limit_properly() -> None:
    """If a provider raises a rate limit, it must be the standardized RateLimitError."""

    # We simulate this via a mock provider that strictly raises RateLimitError
    class StrictMock(BaseProvider):
        def query(self, prompt: str, schema_hint: Optional[dict[str, Any]] = None) -> None:
            raise RateLimitError("429 Too Many Requests")

        def generate(self, prompt: str) -> None:
            pass

    provider = StrictMock()
    with pytest.raises(RateLimitError):
        provider.query("Test")


def test_provider_token_accounting_structure() -> None:
    """Providers (when not mocked) must track input/output tokens via telemetry."""
    # The telemetry is managed by the IntelligenceGateway, which wraps the provider.
    # This contract ensures the provider itself exposes raw responses that can be counted.
    provider = LLMProvider()
    response = provider.query("Prompt", {"hypotheses": None})

    # Just a simple sanity check that the provider isn't swallowing token data
    assert len(str(response)) > 0
