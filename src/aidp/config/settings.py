from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentSettings(BaseSettings):
    """
    Application settings, automatically loaded from environment variables and .env file.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Provider Keys
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    PUBMED_API_KEY: str | None = None
    SEMANTIC_SCHOLAR_API_KEY: str | None = None
    OPENALEX_API_KEY: str | None = None
    ARXIV_API_KEY: str | None = None

    # Global Settings
    ENVIRONMENT: str = "production"
    LOG_LEVEL: str = "INFO"
    
    # Provider Execution Configurations
    DEFAULT_TIMEOUT_SEC: int = 30
    MAX_RETRIES: int = 3
    RATE_LIMIT_DELAY_SEC: int = 5

def get_settings() -> EnvironmentSettings:
    return EnvironmentSettings()
