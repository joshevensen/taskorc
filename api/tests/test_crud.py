"""Happy-path CRUD tests for every endpoint group."""
from httpx import AsyncClient


# ── Users ──────────────────────────────────────────────────────────────────────

async def test_get_me(async_client: AsyncClient, auth_headers: dict):
    resp = await async_client.get("/users/me", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["email"].endswith("@example.com")


async def test_patch_me(async_client: AsyncClient, auth_headers: dict):
    resp = await async_client.patch(
        "/users/me", json={"founder_notes": "Initial thoughts"}, headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["founder_notes"] == "Initial thoughts"


# ── Projects ───────────────────────────────────────────────────────────────────

async def test_create_project(async_client: AsyncClient, auth_headers: dict):
    resp = await async_client.post(
        "/projects", json={"name": "My Project"}, headers=auth_headers
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "My Project"


async def test_list_projects(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    resp = await async_client.get("/projects", headers=auth_headers)
    assert resp.status_code == 200
    ids = [p["id"] for p in resp.json()]
    assert str(seeded_data["project"].id) in ids


async def test_get_project(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    pid = seeded_data["project"].id
    resp = await async_client.get(f"/projects/{pid}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == str(pid)


async def test_patch_project(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    pid = seeded_data["project"].id
    resp = await async_client.patch(
        f"/projects/{pid}", json={"description": "Updated"}, headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["description"] == "Updated"


# ── Tasks ──────────────────────────────────────────────────────────────────────

async def test_create_task(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    pid = seeded_data["project"].id
    resp = await async_client.post(
        f"/projects/{pid}/tasks",
        json={"title": "New Task", "status": "planned"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.json()["title"] == "New Task"


async def test_list_tasks(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    pid = seeded_data["project"].id
    resp = await async_client.get(f"/projects/{pid}/tasks", headers=auth_headers)
    assert resp.status_code == 200
    ids = [t["id"] for t in resp.json()]
    assert str(seeded_data["task"].id) in ids


async def test_get_task(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    tid = seeded_data["task"].id
    resp = await async_client.get(f"/tasks/{tid}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == str(tid)


async def test_patch_task(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    tid = seeded_data["task"].id
    resp = await async_client.patch(
        f"/tasks/{tid}", json={"description": "Updated"}, headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["description"] == "Updated"


async def test_put_subtasks(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    tid = seeded_data["task"].id
    subtasks = [{"id": "s1", "description": "Do X", "prompt": "Do X", "completed": False}]
    resp = await async_client.put(
        f"/tasks/{tid}/subtasks", json=subtasks, headers=auth_headers
    )
    assert resp.status_code == 200
    assert len(resp.json()["subtasks"]) == 1


async def test_complete_subtask(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    tid = seeded_data["task"].id
    subtasks = [{"id": "s1", "description": "Do X", "prompt": "Do X", "completed": False}]
    await async_client.put(f"/tasks/{tid}/subtasks", json=subtasks, headers=auth_headers)
    resp = await async_client.post(
        f"/tasks/{tid}/subtasks/s1/complete", headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["subtasks"][0]["completed"] is True


# ── Notes ──────────────────────────────────────────────────────────────────────

async def test_create_note(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    pid = seeded_data["project"].id
    resp = await async_client.post(
        f"/projects/{pid}/notes",
        json={"title": "New Note", "body": "Body text", "category": "general"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.json()["title"] == "New Note"


async def test_list_notes(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    pid = seeded_data["project"].id
    resp = await async_client.get(f"/projects/{pid}/notes", headers=auth_headers)
    assert resp.status_code == 200
    ids = [n["id"] for n in resp.json()]
    assert str(seeded_data["note"].id) in ids


async def test_get_note(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    nid = seeded_data["note"].id
    resp = await async_client.get(f"/notes/{nid}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == str(nid)


async def test_patch_note(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    nid = seeded_data["note"].id
    resp = await async_client.patch(
        f"/notes/{nid}", json={"body": "Updated body"}, headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["body"] == "Updated body"


async def test_delete_note(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    pid = seeded_data["project"].id
    create = await async_client.post(
        f"/projects/{pid}/notes",
        json={"title": "To Delete", "body": "bye", "category": "general"},
        headers=auth_headers,
    )
    nid = create.json()["id"]
    resp = await async_client.delete(f"/notes/{nid}", headers=auth_headers)
    assert resp.status_code == 204


# ── Logs ───────────────────────────────────────────────────────────────────────

async def test_create_log(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    pid = seeded_data["project"].id
    resp = await async_client.post(
        f"/projects/{pid}/logs",
        json={"skill": "orc-build", "outcome": "success"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.json()["skill"] == "orc-build"


async def test_list_logs(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    pid = seeded_data["project"].id
    await async_client.post(
        f"/projects/{pid}/logs",
        json={"skill": "orc-build", "outcome": "success"},
        headers=auth_headers,
    )
    resp = await async_client.get(f"/projects/{pid}/logs", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


# ── Artifacts ──────────────────────────────────────────────────────────────────

async def test_create_artifact(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    pid = seeded_data["project"].id
    resp = await async_client.post(
        "/artifacts",
        json={
            "title": "Spec Doc",
            "url": "https://example.com/doc",
            "type": "document",
            "parent_type": "project",
            "parent_id": str(pid),
        },
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.json()["title"] == "Spec Doc"


async def test_list_artifacts(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    pid = seeded_data["project"].id
    await async_client.post(
        "/artifacts",
        json={
            "title": "Doc",
            "url": "https://example.com",
            "type": "document",
            "parent_type": "project",
            "parent_id": str(pid),
        },
        headers=auth_headers,
    )
    resp = await async_client.get(
        "/artifacts", params={"parent_type": "project", "parent_id": str(pid)},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


async def test_get_artifact(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    pid = seeded_data["project"].id
    create = await async_client.post(
        "/artifacts",
        json={
            "title": "Doc",
            "url": "https://example.com",
            "type": "document",
            "parent_type": "project",
            "parent_id": str(pid),
        },
        headers=auth_headers,
    )
    aid = create.json()["id"]
    resp = await async_client.get(f"/artifacts/{aid}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == aid


async def test_patch_artifact(async_client: AsyncClient, auth_headers: dict, seeded_data: dict):
    pid = seeded_data["project"].id
    create = await async_client.post(
        "/artifacts",
        json={
            "title": "Doc",
            "url": "https://example.com",
            "type": "document",
            "parent_type": "project",
            "parent_id": str(pid),
        },
        headers=auth_headers,
    )
    aid = create.json()["id"]
    resp = await async_client.patch(
        f"/artifacts/{aid}", json={"title": "Updated Doc"}, headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated Doc"
