import pytest

from aidp.intelligence.providers.base import RateLimitError
from aidp.intelligence.providers.mock import MockProvider


def test_mock_provider_success() -> None:
    provider = MockProvider(fail_count=0)
    response = provider.generate("Test prompt")

    assert response.usage.input_tokens == 11
    assert response.usage.total_cost_usd > 0
    assert response.opinion.belief == 0.8
    assert provider.current_attempts == 1


def test_mock_provider_retry_recovery() -> None:
    # Fails twice, succeeds on the third attempt
    provider = MockProvider(fail_count=2)
    response = provider.generate("Test prompt with retries")

    assert response.opinion.belief == 0.8
    assert provider.current_attempts == 3


def test_mock_provider_retry_exhaustion() -> None:
    # Fails 4 times, but max_retries is 3 in the decorator
    provider = MockProvider(fail_count=4)
    with pytest.raises(RateLimitError):
        provider.generate("Test prompt that dies")

    assert provider.current_attempts == 4  # Initial + 3 retries
