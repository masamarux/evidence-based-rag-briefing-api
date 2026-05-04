from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Evidence-Based RAG Briefing API"
    app_env: str = "development"

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "evidence_rag"
    postgres_password: str = "evidence_rag"
    postgres_db: str = "evidence_rag_db"

    database_url: str | None = None

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimensions: int = 384

    llm_provider: str | None = None
    llm_api_key: str | None = None
    llm_model: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()