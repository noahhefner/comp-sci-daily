import os
from functools import lru_cache

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = ConfigDict(case_sensitive=False)

    auth0_domain: str
    auth0_client_id: str


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings(
        auth0_domain=os.getenv("AUTH0_DOMAIN", ""),
        auth0_client_id=os.getenv("AUTH0_CLIENT_ID", ""),
    )
