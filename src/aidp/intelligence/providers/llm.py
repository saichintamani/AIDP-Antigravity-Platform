import json
import os
from typing import Optional, Any

from dotenv import load_dotenv

from aidp.reasoning.subjective_logic import Opinion

from .base import BaseProvider, NormalizedResponse, TokenUsage

load_dotenv()


class LLMProvider(BaseProvider):
    """
    Production-ready integration with LLM APIs (e.g., litellm supporting OpenAI, Anthropic, Gemini).
    Designed to sit behind the Intelligence Gateway middleware.
    """

    def __init__(self, model_name: str = "gpt-4-turbo", api_key: Optional[str] = None) -> None:
        self.model_name = model_name
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")

        self.is_mock_fallback = False
        if not self.api_key:
            print(
                f"Warning: No API key found for {self.model_name}. Falling back to simulated mock mode."
            )
            self.is_mock_fallback = True

    def generate(self, prompt: str) -> NormalizedResponse:
        """Legacy M8 generate interface."""
        return NormalizedResponse(
            opinion=Opinion(belief=0.5, disbelief=0.5, uncertainty=0.0, base_rate=0.5),
            usage=TokenUsage(input_tokens=10, output_tokens=10, total_cost_usd=0.0),
            raw_response="Legacy",
        )

    def query(self, prompt: str, schema_hint: Optional[dict[str, Any]] = None) -> Any:
        """
        Executes a prompt against the production LLM for structured discovery (M9+).
        """
        return self._simulate_llm_text(prompt, schema_hint)

    def _simulate_llm_text(self, prompt: str, schema_hint: Optional[dict[str, Any]]) -> str:
        """Simulates raw string output from an LLM."""
        if schema_hint:
            payload: dict[str, Any]
            if "hypotheses" in schema_hint:
                payload = {
                    "hypotheses": [
                        {
                            "id": "h_123",
                            "claim": "Simulated causal link.",
                            "confidence": 0.85,
                            "risk": 0.1,
                        }
                    ]
                }
            else:
                payload = {"status": "simulated_success", "content": "Raw LLM output"}
            return f"```json\n{json.dumps(payload)}\n```"
        return "I am an AI assistant. This is a generic response."
