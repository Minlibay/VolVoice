"""FastAPI startup hooks."""

from fastapi import FastAPI

from src.volvoice.infrastructure.audio import AudioTransportFactory


def register_startup_event(app: FastAPI) -> None:
    """Register startup event handlers on the application."""

    @app.on_event("startup")
    async def _startup() -> None:
        # Initialize audio transport factory for warm cache.
        app.state.audio_transport_factory = AudioTransportFactory()

    @app.on_event("shutdown")
    async def _shutdown() -> None:
        # Reserved for future cleanup of audio workers or DB connections.
        if hasattr(app.state, "audio_transport_factory"):
            delattr(app.state, "audio_transport_factory")