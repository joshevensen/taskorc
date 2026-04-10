"""Tests for authentication endpoints and token lifecycle."""
from httpx import AsyncClient


async def test_create_token_returns_orc_prefixed_token(async_client: AsyncClient):
    resp = await async_client.post(
        "/auth/token", json={"name": "Alice", "email": "alice@example.com"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "token" in data
    assert data["token"].startswith("orc_")


async def test_get_me_with_valid_token(async_client: AsyncClient, auth_headers: dict):
    resp = await async_client.get("/users/me", headers=auth_headers)
    assert resp.status_code == 200
    assert "id" in resp.json()


async def test_get_me_with_tampered_token(async_client: AsyncClient):
    resp = await async_client.get(
        "/users/me", headers={"Authorization": "Bearer orc_tampered000000000000"}
    )
    assert resp.status_code == 401


async def test_get_me_with_no_auth_header(async_client: AsyncClient):
    resp = await async_client.get("/users/me")
    assert resp.status_code == 401


async def test_revoke_token(async_client: AsyncClient, auth_headers: dict):
    resp = await async_client.delete("/auth/token", headers=auth_headers)
    assert resp.status_code == 200


async def test_revoked_token_rejected(async_client: AsyncClient, auth_headers: dict):
    await async_client.delete("/auth/token", headers=auth_headers)
    resp = await async_client.get("/users/me", headers=auth_headers)
    assert resp.status_code == 401
