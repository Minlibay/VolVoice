"""Health and readiness endpoints."""

from fastapi import APIRouter

from src.volvoice.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health", summary="Service liveness probe")
def health_check() -> dict[str, str]:
    """Return a simple liveness payload."""

    settings = get_settings()
    return {"status": "ok", "service": settings.app_name}


@router.get("/version", summary="Service version information")
def version() -> dict[str, str]:
    """Return static version details."""

    return {"version": "0.1.0"}