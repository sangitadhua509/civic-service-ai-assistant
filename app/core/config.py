"""
This file reads values from your .env file (or environment variables)
and makes them available everywhere in the app as `settings.SOMETHING`.

Why do this instead of hard-coding values?
- Different people (or servers) can use different databases/keys
  without changing code.
- Secrets never get typed directly into source files.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Civic Service AI Assistant"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # These will actually be used starting Phase 3 (database) and Phase 4 (auth).
    # Giving them safe defaults now means the app doesn't crash if they're
    # missing from .env yet.
    DATABASE_URL: str = ""
    JWT_SECRET_KEY: str = "temporary-dev-secret-change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Other files will do: `from app.core.config import settings`
settings = Settings()
