"""Application settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Project settings loaded from environment variables."""

    app_name: str = "Currency Rates ETL API"
    cbr_rates_url: str = "https://www.cbr.ru/scripts/XML_daily.asp"

    postgres_user: str = "currency_user"
    postgres_password: str = "currency_password"
    postgres_db: str = "currency_rates"
    postgres_host: str = "postgres"
    postgres_port: int = 5432

    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def database_url(self) -> str:
        """Build PostgreSQL URL for SQLAlchemy."""
        return (
            "postgresql+psycopg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
