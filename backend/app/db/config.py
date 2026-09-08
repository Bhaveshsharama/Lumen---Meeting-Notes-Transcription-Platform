"""
db/config.py — Application configuration loaded from environment variables.
Keeps all env-var reads in one place (SRP), so no other module touches os.environ directly.
"""

from pydantic_settings import BaseSettings
from pathlib import Path
import os
from dotenv import load_dotenv

# backend/app/db/config.py → backend/ is 3 levels up
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent

env_path = BACKEND_DIR / ".env"
load_dotenv(dotenv_path=env_path, override=True)

_DEFAULT_DB = f"sqlite:///{BACKEND_DIR / 'fireflies.db'}".replace("\\", "/")


class Settings(BaseSettings):
    """
    Single source of truth for configuration.
    All values read from environment variables / .env file.
    """

    # Database — reads DATABASE_URL env var; falls back to absolute local SQLite path
    DATABASE_URL: str = os.getenv("DATABASE_URL", _DEFAULT_DB)

    # Groq API key — NEVER hardcoded; empty string means LLM falls back to Mock
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # CORS — comma-separated list in CORS_ORIGINS env var, e.g. "https://lumen.app,https://www.lumen.app"
    # Falls back to localhost:3000 for local development
    CORS_ORIGINS: list[str] = [
        o.strip()
        for o in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
        if o.strip()
    ]

    model_config = {
        "env_file": str(BACKEND_DIR / ".env"),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


# Singleton instance used throughout the app
settings = Settings()
