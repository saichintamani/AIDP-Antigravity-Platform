import json
import os
from typing import Any

from dotenv import load_dotenv

from aidp.reasoning.subjective_logic import Opinion

from .base import BaseProvider, NormalizedResponse, TokenUsage

load_dotenv()


class LLMProvider(BaseProvider):
    """
    Production-ready integration with LLM APIs (e.g., litellm supporting OpenAI, Anthropic, Gemini).
    Designed to sit behind the Intelligence Gateway middleware.
    """

    def __init__(self, model_name: str = "gpt-4o-mini", api_key: str | None = None) -> None:
        self.model_name = model_name
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY") or "dummy"

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

    def query(self, prompt: str, schema_hint: dict[str, Any] | None = None) -> Any:
        """
        Executes a prompt against the production LLM for structured discovery (M9+).
        """
        import litellm
        
        try:
            kwargs = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "num_ctx": 4096,
            }
            if schema_hint:
                model_lower = self.model_name.lower()
                if "gemini" in model_lower:
                    # Gemini (and OpenAI) Strict Structured Outputs
                    kwargs["response_format"] = {
                        "type": "json_schema",
                        "json_schema": {
                            "name": "aidp_schema",
                            "schema": schema_hint,
                            "strict": True
                        }
                    }
                elif "gemma" in model_lower:
                    # Gemma lacks strict JSON decoding natively on some endpoints. Force via prompt engineering.
                    constraint = (
                        "\n\n[CRITICAL: You MUST output ONLY raw JSON exactly matching this schema. "
                        f"NO markdown formatting (no ```json), NO text outside the JSON.]\n{json.dumps(schema_hint)}"
                    )
                    kwargs["messages"][0]["content"] += constraint
                    # Still try to enable JSON mode if the runtime supports it
                    kwargs["response_format"] = {"type": "json_object"}
                else:
                    # Standard JSON mode fallback
                    kwargs["response_format"] = {"type": "json_object"}
                
            response = litellm.completion(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            if self.is_mock_fallback:
                return self._simulate_llm_text(prompt, schema_hint)
            raise RuntimeError(f"litellm provider query failed: {e}")

    def _simulate_llm_text(self, prompt: str, schema_hint: dict[str, Any] | None) -> str:
        """Simulates raw string output from an LLM when in mock mode and failing."""
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
