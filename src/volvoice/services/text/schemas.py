"""Pydantic schemas for future text channel APIs."""

from pydantic import BaseModel, Field


class TextChannelBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    topic: str | None = Field(default=None, max_length=1024)


class TextChannelCreate(TextChannelBase):
    """Schema for text channel creation requests."""


class TextChannelResponse(TextChannelBase):
    id: str = Field(..., description="Unique identifier for the text channel")
    status: str = Field(default="pending", description="Implementation status flag")


__all__ = ["TextChannelCreate", "TextChannelResponse"]