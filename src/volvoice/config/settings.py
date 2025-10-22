"""Application settings management."""

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Centralized application settings.

    Values are loaded from environment variables and optional `.env` files to support local
    development on Windows.
    """

    app_name: str = "VolVoice"
    debug: bool = True
    database_url: str = Field(
        default="sqlite+aiosqlite:///./volvoice.db",
        description="SQLAlchemy database URL for persistence layer.",
    )
    allow_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost", "http://127.0.0.1"],
        description="CORS allowed origins",
    )
    voice_sample_rate: int = 48000
    voice_frame_duration_ms: int = 20
    max_concurrent_voice_rooms: int = 100
    text_channels_enabled: bool = False
    assets_dir: Path = Path("assets")
    windows_audio_device: Optional[str] = Field(
        default=None,
        description="Preferred Windows audio device identifier.",
    )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


@lru_cache
def get_settings() -> Settings:
    """Return the cached settings instance."""

    return Settings()


__all__ = ["Settings", "get_settings"]