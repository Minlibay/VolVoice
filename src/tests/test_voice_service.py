"""Tests for the in-memory voice room service."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("pydantic")

from fastapi import HTTPException

from volvoice.config.settings import Settings
from volvoice.services.voice.schemas import VoiceRoomCreate
from volvoice.services.voice.service import VoiceRoomService


class _StubClientState:
    """Minimal stand-in for ``starlette.websockets.WebSocketState``."""

    CONNECTED = "CONNECTED"

    def __init__(self, value: str = CONNECTED) -> None:
        self.value = value

    def __eq__(self, other: object) -> bool:  # pragma: no cover - trivial
        if isinstance(other, _StubClientState):
            return self.value == other.value
        return self.value == other


class StubWebSocket:
    """Test double that mimics the subset of WebSocket behaviour the service relies on."""

    def __init__(self) -> None:
        self.accepted = False
        self.closed: list[tuple[int, str]] = []
        self.sent_bytes: list[bytes] = []
        self.sent_text: list[str] = []
        self.state = SimpleNamespace()
        self.client_state: _StubClientState | str = _StubClientState()
        self._receive_queue: asyncio.Queue[dict[str, object]] = asyncio.Queue()

    async def accept(self) -> None:
        self.accepted = True

    async def close(self, code: int, reason: str) -> None:
        self.closed.append((code, reason))
        self.client_state = _StubClientState("DISCONNECTED")

    async def receive(self) -> dict[str, object]:
        return await self._receive_queue.get()

    def queue_message(self, message: dict[str, object]) -> None:
        self._receive_queue.put_nowait(message)

    async def send_bytes(self, data: bytes) -> None:
        self.sent_bytes.append(data)

    async def send_text(self, data: str) -> None:
        self.sent_text.append(data)


@pytest.mark.asyncio
async def test_create_and_list_rooms_sorted() -> None:
    settings = Settings(max_concurrent_voice_rooms=10)
    service = VoiceRoomService(settings=settings)

    first = await service.create_room(VoiceRoomCreate(name="Alpha", bitrate=64000))
    second = await service.create_room(VoiceRoomCreate(name="Beta", bitrate=64000))

    rooms = await service.list_rooms()

    assert [room.id for room in rooms] == [first.id, second.id]


@pytest.mark.asyncio
async def test_room_limit_enforced() -> None:
    settings = Settings(max_concurrent_voice_rooms=1)
    service = VoiceRoomService(settings=settings)

    await service.create_room(VoiceRoomCreate(name="Main", bitrate=64000))

    with pytest.raises(HTTPException) as exc:
        await service.create_room(VoiceRoomCreate(name="Overflow", bitrate=64000))

    assert exc.value.status_code == 429


@pytest.mark.asyncio
async def test_broadcast_text_between_participants() -> None:
    settings = Settings(max_concurrent_voice_rooms=2)
    service = VoiceRoomService(settings=settings)
    room = await service.create_room(VoiceRoomCreate(name="Stage", bitrate=64000))

    sender = StubWebSocket()
    receiver = StubWebSocket()

    await service.register_socket(room.id, sender)
    await service.register_socket(room.id, receiver)

    sender.queue_message({"text": "ping"})
    sender.queue_message({"type": "websocket.disconnect"})

    await service.run_socket_session(room.id, sender)

    assert receiver.sent_text == ["ping"]

    await service.unregister_socket(room.id, sender)
    await service.unregister_socket(room.id, receiver)