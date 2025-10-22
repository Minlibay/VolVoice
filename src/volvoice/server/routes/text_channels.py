"""Placeholder routes for future text channel support."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ...services.text import TextChannelService, get_text_channel_service
from ...services.text.schemas import TextChannelCreate, TextChannelResponse

router = APIRouter(tags=["text channels"])


@router.post("/channels", response_model=TextChannelResponse, status_code=202)
async def create_text_channel(
    payload: TextChannelCreate,
    service: Annotated[TextChannelService, Depends(get_text_channel_service)],
) -> TextChannelResponse:
    """Accept a request to create a text channel.

    The endpoint currently raises an informative error to clarify that text support is not yet
    available while preserving the public API surface.
    """

    raise HTTPException(status_code=501, detail="Text channels are not yet implemented")


@router.get("/channels", response_model=list[TextChannelResponse])
async def list_text_channels(
    service: Annotated[TextChannelService, Depends(get_text_channel_service)],
) -> list[TextChannelResponse]:
    """Return a placeholder response for future text channel listings."""

    raise HTTPException(status_code=501, detail="Text channels are not yet implemented")