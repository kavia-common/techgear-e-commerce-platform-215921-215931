from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Uses BaseSettings to load configuration from environment variables with sensible defaults.
    DATABASE_URL defaults to a local SQLite database file for development purposes.
    """

    APP_NAME: str = "TechGear E-Commerce Backend"
    API_VERSION: str = "0.1.0"

    # Database
    DATABASE_URL: str = "sqlite:///./ecommerce.db"

    # Security
    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"  # Instructions: set via environment in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    ALGORITHM: str = "HS256"

    # CORS: can be set as comma-separated env var BACKEND_CORS_ORIGINS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Seeding
    SEED_DATA_ON_STARTUP: bool = True

    class Config:
        env_file = ".env"
        extra = "ignore"

    def model_post_init(self, __context) -> None:
        """Normalize comma-separated CORS origins to list when provided as env var."""
        cors_env = os.getenv("BACKEND_CORS_ORIGINS")
        if cors_env and isinstance(self.BACKEND_CORS_ORIGINS, list):
            # If env provided as comma-separated string, split and strip
            parts = [p.strip() for p in cors_env.split(",") if p.strip()]
            if parts:
                self.BACKEND_CORS_ORIGINS = parts  # type: ignore


# PUBLIC_INTERFACE
def get_settings() -> Settings:
    """Return cached settings instance loaded from environment."""
    return _get_cached_settings()


@lru_cache()
def _get_cached_settings() -> Settings:
    return Settings()
