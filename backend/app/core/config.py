"""
SentinelAI — Core Configuration

Centralized settings using pydantic-settings with .env loading.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "SentinelAI Mission Control"
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "change-me-in-production"
    api_v1_prefix: str = "/api/v1"

    # PostgreSQL
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_user: str = "sentinel"
    postgres_password: str = "sentinel_secret_2024"
    postgres_db: str = "sentinel_db"
    database_url: str = "postgresql+asyncpg://sentinel:sentinel_secret_2024@postgres:5432/sentinel_db"

    # Redis
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_url: str = "redis://redis:6379/0"

    # Celery
    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/1"

    # ChromaDB
    chroma_host: str = "chromadb"
    chroma_port: int = 8000

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    openai_embedding_model: str = "text-embedding-3-small"

    # Rate limiting
    rate_limit_per_minute: int = 60

    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:8080"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def sync_database_url(self) -> str:
        return self.database_url.replace("+asyncpg", "")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
