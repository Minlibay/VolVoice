"""Domain models for voice rooms."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Set


@dataclass(slots=True)
class VoiceRoom:
    """Representation of a voice room in memory."""

    id: str
    name: str
    bitrate: int
    user_limit: int | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    session_ids: Set[str] = field(default_factory=set)

    def as_dict(self) -> Dict[str, object]:
        """Serialize room attributes into a dictionary."""

        return {
            "id": self.id,
            "name": self.name,
            "bitrate": self.bitrate,
            "user_limit": self.user_limit,
            "created_at": self.created_at,
            "active_sessions": len(self.session_ids),
        }


__all__ = ["VoiceRoom"]