"""Placeholder text channel service."""

from dataclasses import dataclass
from typing import ClassVar


@dataclass(slots=True)
class TextChannelService:
    """Service scaffolding for future text channel functionality."""

    message: ClassVar[str] = "Text channels are scheduled for a future release."

    async def list_channels(self) -> list[dict[str, str]]:
        """Placeholder asynchronous list call."""

        return []

    async def create_channel(self, name: str) -> dict[str, str]:
        """Placeholder asynchronous creation call."""

        return {"name": name, "status": "pending"}


def get_text_channel_service() -> TextChannelService:
    """Return a singleton text channel service instance."""

    # Stateless placeholder for now; instantiate on demand.
    return TextChannelService()