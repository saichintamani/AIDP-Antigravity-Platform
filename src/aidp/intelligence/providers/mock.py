from typing import Any

from aidp.intelligence.providers.base import (
    BaseProvider,
    NormalizedResponse,
    RateLimitError,
    TokenUsage,
)
from aidp.intelligence.providers.middleware import with_retry
from aidp.reasoning.subjective_logic import Opinion


class MockProvider(BaseProvider):
    """
    A simulated provider used for testing retry mechanisms and rate limiting.
    """

    def __init__(self, fail_count: int = 0) -> None:
        self.fail_count = fail_count
        self.current_attempts = 0
        self.cost_per_1k_tokens = 0.002
        self.model_name = "mock-provider-v1"
        self.default_params: dict[str, Any] = {}

    @with_retry(max_retries=3, base_delay=0.1)  # Fast delay for tests
    def generate(self, prompt: str) -> NormalizedResponse:
        self.current_attempts += 1

        # Simulate synthetic 429 failures
        if self.current_attempts <= self.fail_count:
            raise RateLimitError(
                f"Simulated 429 Too Many Requests (Attempt {self.current_attempts})"
            )

        # Standard fake response
        input_len = len(prompt)
        usage = TokenUsage(
            input_tokens=input_len,
            output_tokens=50,
            total_cost_usd=((input_len + 50) / 1000) * self.cost_per_1k_tokens,
        )

        opinion = Opinion(belief=0.8, disbelief=0.1, uncertainty=0.1, base_rate=0.5)

        return NormalizedResponse(
            opinion=opinion, usage=usage, raw_response="Simulated structured LLM output."
        )

    def query(self, prompt: str, schema_hint: dict[str, Any] | None = None) -> str:
        """Simulate the M9+ query interface."""
        self.current_attempts += 1

        # Simulate synthetic 429 failures
        if self.current_attempts <= self.fail_count:
            raise RateLimitError(
                f"Simulated 429 Too Many Requests (Attempt {self.current_attempts})"
            )

        import json

        if schema_hint:
            from pydantic import BaseModel
            if isinstance(schema_hint, type) and issubclass(schema_hint, BaseModel):
                keys = schema_hint.model_fields.keys()
            elif isinstance(schema_hint, dict):
                keys = schema_hint.keys()
            else:
                keys = []
            
            # We just return a JSON string with nulls matching the schema keys to pass validation
            payload = dict.fromkeys(keys, "mock_string")
            # But the test harness relies on validation failing for `mock_a` so we should just return a generic JSON
            return f"```json\n{json.dumps(payload)}\n```"

        return '{"result": "mock_success"}'
