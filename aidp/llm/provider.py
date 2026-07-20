"""LLM provider abstraction for AIDP.

Wraps `litellm` calls and reads configuration from the central settings.
"""

import os
import litellm
from aidp.config.settings import Settings
from aidp.utils.logger import get_logger

logger = get_logger(__name__)

class LLMProvider:
    """Simple synchronous LLM provider.

    The model name defaults to the `AIDP_LLM_MODEL` environment variable or
    ``gpt-4o-mini`` if not set.
    """

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or Settings()
        self.model = self.settings.llm_model
        self.temperature = self.settings.llm_temperature
        self.max_tokens = self.settings.llm_max_tokens
        logger.info("LLMProvider initialized", model=self.model)

    def query(self, prompt: str) -> dict:
        """Send a prompt to the LLM and return the parsed JSON response.

        This method mirrors the original `_call_llm` helper but uses the
        configured model and temperature.
        """
        response = litellm.completion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            response_format={"type": "json_object"},
            max_tokens=self.max_tokens,
        )
        content = response.choices[0].message.content.strip()
        try:
            return json.loads(content)
        except Exception as e:
            logger.error("Failed to parse LLM JSON response", error=str(e))
            raise
