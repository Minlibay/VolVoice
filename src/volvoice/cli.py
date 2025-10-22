"""Command line tooling for VolVoice."""

from __future__ import annotations

import asyncio
from typing import Optional

import typer

from .services.voice import get_voice_room_service
from .services.voice.schemas import VoiceRoomCreate

cli = typer.Typer(help="VolVoice administration commands")


def _run_async(coro):
    return asyncio.run(coro)


@cli.command("create-room")
def create_room(
    name: str = typer.Argument(..., help="Name of the voice room"),
    bitrate: int = typer.Option(64000, help="Target bitrate for the room"),
    user_limit: Optional[int] = typer.Option(None, help="Optional user limit"),
) -> None:
    """Create a voice room using the in-memory service."""

    service = get_voice_room_service()
    payload = VoiceRoomCreate(name=name, bitrate=bitrate, user_limit=user_limit)
    room = _run_async(service.create_room(payload))
    typer.echo(f"Created room {room.id} ({room.name})")


@cli.command("list-rooms")
def list_rooms() -> None:
    """List all voice rooms."""

    service = get_voice_room_service()
    rooms = _run_async(service.list_rooms())
    if not rooms:
        typer.echo("No voice rooms available.")
        raise typer.Exit(code=0)

    for room in rooms:
        typer.echo(
            f"- {room.id}: {room.name} | bitrate={room.bitrate} | active={room.active_sessions}"
        )


if __name__ == "__main__":
    cli()