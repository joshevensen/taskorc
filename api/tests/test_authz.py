"""Authorization tests: user B cannot access user A's resources."""
from uuid import uuid4

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import generate_pat, hash_pat
from app.models.user import User


@pytest_asyncio.fixture
async def user_b_headers(db_session: AsyncSession):
    pat = generate_pat()
    user = User(
        name="User B",
        email=f"userb-{uuid4()}@example.com",
        pat_hash=hash_pat(pat),
    )
    db_session.add(user)
    await db_session.commit()
    return {"Authorization": f"Bearer {pat}"}


async def test_get_project_forbidden(
    async_client: AsyncClient, seeded_data: dict, user_b_headers: dict
):
    pid = seeded_data["project"].id
    resp = await async_client.get(f"/projects/{pid}", headers=user_b_headers)
    assert resp.status_code == 403


async def test_patch_project_forbidden(
    async_client: AsyncClient, seeded_data: dict, user_b_headers: dict
):
    pid = seeded_data["project"].id
    resp = await async_client.patch(
        f"/projects/{pid}", json={"name": "Stolen"}, headers=user_b_headers
    )
    assert resp.status_code == 403


async def test_get_task_forbidden(
    async_client: AsyncClient, seeded_data: dict, user_b_headers: dict
):
    tid = seeded_data["task"].id
    resp = await async_client.get(f"/tasks/{tid}", headers=user_b_headers)
    assert resp.status_code == 403


async def test_patch_task_forbidden(
    async_client: AsyncClient, seeded_data: dict, user_b_headers: dict
):
    tid = seeded_data["task"].id
    resp = await async_client.patch(
        f"/tasks/{tid}", json={"description": "Stolen"}, headers=user_b_headers
    )
    assert resp.status_code == 403


async def test_get_note_forbidden(
    async_client: AsyncClient, seeded_data: dict, user_b_headers: dict
):
    nid = seeded_data["note"].id
    resp = await async_client.get(f"/notes/{nid}", headers=user_b_headers)
    assert resp.status_code == 403


async def test_delete_note_forbidden(
    async_client: AsyncClient, seeded_data: dict, user_b_headers: dict
):
    nid = seeded_data["note"].id
    resp = await async_client.delete(f"/notes/{nid}", headers=user_b_headers)
    assert resp.status_code == 403


async def test_list_logs_forbidden(
    async_client: AsyncClient, seeded_data: dict, user_b_headers: dict
):
    pid = seeded_data["project"].id
    resp = await async_client.get(f"/projects/{pid}/logs", headers=user_b_headers)
    assert resp.status_code == 403


async def test_create_log_forbidden(
    async_client: AsyncClient, seeded_data: dict, user_b_headers: dict
):
    pid = seeded_data["project"].id
    resp = await async_client.post(
        f"/projects/{pid}/logs",
        json={"skill": "orc-build", "outcome": "success"},
        headers=user_b_headers,
    )
    assert resp.status_code == 403
