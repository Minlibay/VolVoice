"""VolVoice ASGI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from src.volvoice.server.events import register_startup_event
from src.volvoice.server.routes import health, text_channels
from .server.routes import voice_rooms


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    settings = get_settings()
    app = FastAPI(title=settings.app_name, debug=settings.debug)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(voice_rooms.router, prefix="/voice")
    app.include_router(text_channels.router, prefix="/text", include_in_schema=False)

    register_startup_event(app)

    return app


app = create_app()