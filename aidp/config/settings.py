from pathlib import Path
from typing import Any, Dict, Optional
import yaml
from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    """Application configuration for AIDP.

    Values are first loaded from an optional ``settings.yaml`` at the project root,
    then overridden by environment variables (via Pydantic's ``BaseSettings``).
    """

    # Core paths
    project_root: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2])
    data_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2] / "data")

    # LLM defaults
    ai_model: str = Field(default="gpt-4o-mini", env="AIDP_LLM_MODEL")
    ai_temperature: float = Field(default=0.7, env="AIDP_LLM_TEMPERATURE")
    max_llm_retries: int = Field(default=3, env="AIDP_MAX_LLM_RETRIES")

    # Observability defaults
    otel_exporter: str = Field(default="console", env="AIDP_OTEL_EXPORTER")  # console | otlp | jaeger
    otel_endpoint: Optional[str] = Field(default=None, env="AIDP_OTEL_ENDPOINT")
    otel_service_name: str = Field(default="aidp", env="AIDP_OTEL_SERVICE_NAME")

    # Plugin configuration
    plugin_namespace: str = Field(default="aidp.plugins", env="AIDP_PLUGIN_NAMESPACE")

    # Arbitrary extra configuration – useful for downstream plugins
    extra: Dict[str, Any] = {}

    @validator("otel_exporter")
    def _validate_exporter(cls, v: str) -> str:
        allowed = {"console", "otlp", "jaeger"}
        if v not in allowed:
            raise ValueError(f"otel_exporter must be one of {allowed}")
        return v

    @classmethod
    def load(cls) -> "Settings":
        """Load settings from ``settings.yaml`` (if present) and environment variables.
        """
        base_path = Path(__file__).resolve().parents[2]
        yaml_file = base_path / "settings.yaml"
        yaml_data: Dict[str, Any] = {}
        if yaml_file.is_file():
            with yaml_file.open("r", encoding="utf-8") as f:
                yaml_data = yaml.safe_load(f) or {}
        return cls(**yaml_data)

# Export a singleton used throughout the codebase
settings = Settings.load()
