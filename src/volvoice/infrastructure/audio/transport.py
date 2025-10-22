"""Audio transport abstractions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class AudioTransport(Protocol):
    """Interface for streaming audio frames between participants."""

    async def send_frame(self, data: bytes) -> None:
        """Send an encoded audio frame."""

    async def receive_frame(self) -> bytes:
        """Receive an encoded audio frame."""


@dataclass(slots=True)
class AudioTransportConfig:
    """Configuration for creating audio transport implementations."""

    codec: str = "opus"
    sample_rate: int = 48000
    frame_duration_ms: int = 20


class AudioTransportFactory:
    """Factory for constructing audio transport instances."""

    def __init__(self, config: AudioTransportConfig | None = None) -> None:
        self._config = config or AudioTransportConfig()

    def create(self) -> AudioTransport:
        """Return a stub transport implementation for development."""

        return _InMemoryAudioTransport()


class _InMemoryAudioTransport:
    """Simplistic in-memory audio transport used for scaffolding."""

    async def send_frame(self, data: bytes) -> None:  # pragma: no cover - placeholder
        del data

    async def receive_frame(self) -> bytes:  # pragma: no cover - placeholder
        return b""


__all__ = ["AudioTransport", "AudioTransportConfig", "AudioTransportFactory"]