"""Basic tests for health endpoints."""

import pytest

pytest.importorskip("fastapi")
httpx = pytest.importorskip("httpx")

from httpx import AsyncClient

from volvoice.main import app


@pytest.mark.asyncio
async def test_health_check() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_version_endpoint() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/version")
    assert response.status_code == 200
    assert response.json()["version"] == "0.1.0"