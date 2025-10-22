"""In-memory voice room service implementation."""

from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import DefaultDict, Dict, Set
from uuid import uuid4

from fastapi import HTTPException, WebSocket

from ...config import Settings, get_settings
from ...domain.models.voice_room import VoiceRoom
from .schemas import VoiceRoomCreate, VoiceRoomResponse


class VoiceRoomService:
    """Manage lifecycle of voice rooms and active websocket sessions."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._rooms: Dict[str, VoiceRoom] = {}
        self._room_sockets: DefaultDict[str, Set[WebSocket]] = defaultdict(set)
        self._lock = asyncio.Lock()

    async def create_room(self, payload: VoiceRoomCreate) -> VoiceRoomResponse:
        """Create a new voice room if capacity permits."""

        async with self._lock:
            if len(self._rooms) >= self._settings.max_concurrent_voice_rooms:
                raise HTTPException(status_code=429, detail="Voice room limit reached")

            room_id = uuid4().hex
            room = VoiceRoom(
                id=room_id,
                name=payload.name,
                bitrate=payload.bitrate,
                user_limit=payload.user_limit,
            )
            self._rooms[room_id] = room

        return VoiceRoomResponse(**room.as_dict())

    async def list_rooms(self) -> list[VoiceRoomResponse]:
        """Return all existing rooms."""

        async with self._lock:
            rooms = [VoiceRoomResponse(**room.as_dict()) for room in self._rooms.values()]
        return sorted(rooms, key=lambda room: room.created_at)

    async def register_socket(self, room_id: str, websocket: WebSocket) -> None:
        """Accept websocket connection and register it to a room."""

        async with self._lock:
            room = self._rooms.get(room_id)
            if room is None:
                await websocket.close(code=4404, reason="Room not found")
                raise HTTPException(status_code=404, detail="Room not found")

            if room.user_limit and len(room.session_ids) >= room.user_limit:
                await websocket.close(code=4403, reason="Room is full")
                raise HTTPException(status_code=403, detail="Room is full")

        await websocket.accept()

        async with self._lock:
            room = self._rooms[room_id]
            self._room_sockets[room_id].add(websocket)
            session_id = uuid4().hex
            room.session_ids.add(session_id)
            websocket.state.session_id = session_id  # type: ignore[attr-defined]

    async def unregister_socket(self, room_id: str, websocket: WebSocket) -> None:
        """Cleanup websocket connection from room."""

        async with self._lock:
            sockets = self._room_sockets.get(room_id)
            if sockets and websocket in sockets:
                sockets.remove(websocket)
                if not sockets:
                    self._room_sockets.pop(room_id, None)
            room = self._rooms.get(room_id)
            session_id = getattr(websocket.state, "session_id", None)
            if room and session_id and session_id in room.session_ids:
                room.session_ids.remove(session_id)

    async def run_socket_session(self, room_id: str, websocket: WebSocket) -> None:
        """Handle a websocket session for broadcasting audio frames.

        Audio frames are represented as binary payloads for now. When text frames arrive (e.g. for
        debugging), the payload is relayed verbatim.
        """

        while True:
            message = await websocket.receive()

            if "bytes" in message and message["bytes"] is not None:
                await self._broadcast_binary(room_id, message["bytes"], websocket)
            elif "text" in message and message["text"] is not None:
                await self._broadcast_text(room_id, message["text"], websocket)
            elif message.get("type") == "websocket.disconnect":
                break

    async def _broadcast_binary(self, room_id: str, payload: bytes, sender: WebSocket) -> None:
        """Broadcast binary payload to room participants."""

        sockets = self._room_sockets.get(room_id, set()).copy()
        if not sockets:
            return
        await asyncio.gather(
            *[
                socket.send_bytes(payload)
                for socket in sockets
                if socket.client_state == socket.client_state.CONNECTED and socket is not sender
            ]
        )

    async def _broadcast_text(self, room_id: str, message: str, sender: WebSocket) -> None:
        """Broadcast text payload to room participants."""

        sockets = self._room_sockets.get(room_id, set()).copy()
        if not sockets:
            return
        await asyncio.gather(
            *[
                socket.send_text(message)
                for socket in sockets
                if socket.client_state == socket.client_state.CONNECTED and socket is not sender
            ]
        )


_voice_room_service: VoiceRoomService | None = None


def get_voice_room_service() -> VoiceRoomService:
    """Provide a singleton voice room service instance."""

    global _voice_room_service
    if _voice_room_service is None:
        _voice_room_service = VoiceRoomService()
    return _voice_room_service


__all__ = ["VoiceRoomService", "get_voice_room_service"]