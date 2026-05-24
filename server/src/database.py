import os
from functools import lru_cache

from pydantic import AliasGenerator, ConfigDict
from pydantic.alias_generators import to_snake
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Database configuration loaded from environment variables."""

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_snake,
        )
    )

    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    @property
    def database_url(self) -> str:
        """Construct PostgreSQL connection URL."""
        return (
            f"postgresql+psycopg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_database_settings() -> DatabaseSettings:
    """Get cached database settings instance."""
    return DatabaseSettings(
        db_host=os.getenv("DB_HOST", "localhost"),
        db_port=int(os.getenv("DB_PORT", "5432")),
        db_user=os.getenv("DB_USER", ""),
        db_password=os.getenv("DB_PASSWORD", ""),
        db_name=os.getenv("DB_NAME", ""),
    )
