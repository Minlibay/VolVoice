"""Voice room API endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect

from ...services.voice import VoiceRoomService, get_voice_room_service
from ...services.voice.schemas import VoiceRoomCreate, VoiceRoomResponse

router = APIRouter(tags=["voice rooms"])


@router.post("/rooms", response_model=VoiceRoomResponse, status_code=201)
async def create_voice_room(
    payload: VoiceRoomCreate,
    service: Annotated[VoiceRoomService, Depends(get_voice_room_service)],
) -> VoiceRoomResponse:
    """Create a new voice room."""

    return await service.create_room(payload)


@router.get("/rooms", response_model=list[VoiceRoomResponse])
async def list_voice_rooms(
    service: Annotated[VoiceRoomService, Depends(get_voice_room_service)],
) -> list[VoiceRoomResponse]:
    """List existing voice rooms."""

    return await service.list_rooms()


@router.websocket("/ws/{room_id}")
async def voice_room_socket(websocket: WebSocket, room_id: str) -> None:
    """Minimal signalling websocket for voice streaming."""

    service = get_voice_room_service()
    try:
        await service.register_socket(room_id, websocket)
    except HTTPException:
        return

    try:
        await service.run_socket_session(room_id, websocket)
    except WebSocketDisconnect:
        pass
    finally:
        await service.unregister_socket(room_id, websocket)