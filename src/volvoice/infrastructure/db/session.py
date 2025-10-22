"""Async database session factory."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from ...config import get_settings

_async_engine: AsyncEngine | None = None
_sessionmaker: async_sessionmaker | None = None


def get_async_engine() -> AsyncEngine:
    """Return a singleton async engine configured from settings."""

    global _async_engine
    if _async_engine is None:
        settings = get_settings()
        _async_engine = create_async_engine(settings.database_url, echo=settings.debug)
    return _async_engine


def get_sessionmaker() -> async_sessionmaker:
    """Return a singleton async sessionmaker."""

    global _sessionmaker
    if _sessionmaker is None:
        _sessionmaker = async_sessionmaker(bind=get_async_engine(), expire_on_commit=False)
    return _sessionmaker


__all__ = ["get_async_engine", "get_sessionmaker"]