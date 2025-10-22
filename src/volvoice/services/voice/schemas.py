"""Pydantic schemas for voice room APIs."""

from datetime import datetime

from pydantic import BaseModel, Field


class VoiceRoomCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    bitrate: int = Field(default=64000, ge=16000, le=384000)
    user_limit: int | None = Field(default=None, ge=2, le=99)


class VoiceRoomResponse(VoiceRoomCreate):
    id: str = Field(..., description="Unique identifier for the voice room")
    created_at: datetime = Field(..., description="ISO timestamp of room creation")
    active_sessions: int = Field(default=0, description="Number of connected participants")


__all__ = ["VoiceRoomCreate", "VoiceRoomResponse"]