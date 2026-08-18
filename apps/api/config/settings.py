"""Projenin bütün ayarlarını tek yerden okuyan sınıf.

Kod içinde hiçbir yerde os.environ ile doğrudan okuma yapılmaz —
herkes bu Settings sınıfını kullanır.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = "local"
    log_level: str = "INFO"
    database_url: str = "postgresql+asyncpg://raguser:ragpass@localhost:5432/agentic_rag"
    redis_url: str = "redis://localhost:6379/0"


settings = Settings()
