"""Business logic tests: /next priority ordering, subtask completion, log append-only."""
from httpx import AsyncClient


# ── Task priority ordering ─────────────────────────────────────────────────────

async def test_next_task_returns_lowest_priority(
    async_client: AsyncClient, auth_headers: dict, seeded_data: dict
):
    pid = seeded_data["project"].id

    # Create three planned tasks with different priorities
    for priority, title in [(10, "Low"), (1, "Highest"), (5, "Mid")]:
        await async_client.post(
            f"/projects/{pid}/tasks",
            json={"title": title, "status": "planned", "priority": priority},
            headers=auth_headers,
        )

    resp = await async_client.get(f"/projects/{pid}/tasks/next", headers=auth_headers)
    assert resp.status_code == 200
    # The seeded_data task has priority 5; "Highest" has priority 1 → should win
    assert resp.json()["title"] == "Highest"


async def test_next_task_excludes_draft_status(
    async_client: AsyncClient, auth_headers: dict, seeded_data: dict
):
    pid = seeded_data["project"].id

    # Create a draft task with very low priority number — should NOT be returned by /next
    await async_client.post(
        f"/projects/{pid}/tasks",
        json={"title": "Draft Task", "status": "draft", "priority": 0},
        headers=auth_headers,
    )
    resp = await async_client.get(f"/projects/{pid}/tasks/next", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["title"] != "Draft Task"


# ── Subtask completion ─────────────────────────────────────────────────────────

async def test_complete_subtask_marks_only_target(
    async_client: AsyncClient, auth_headers: dict, seeded_data: dict
):
    pid = seeded_data["project"].id

    create = await async_client.post(
        f"/projects/{pid}/tasks",
        json={"title": "Task With Subtasks", "status": "planned"},
        headers=auth_headers,
    )
    tid = create.json()["id"]

    subtasks = [
        {"id": "s1", "description": "First", "prompt": "Do first", "completed": False},
        {"id": "s2", "description": "Second", "prompt": "Do second", "completed": False},
    ]
    await async_client.put(f"/tasks/{tid}/subtasks", json=subtasks, headers=auth_headers)
    await async_client.post(f"/tasks/{tid}/subtasks/s1/complete", headers=auth_headers)

    resp = await async_client.get(f"/tasks/{tid}", headers=auth_headers)
    assert resp.status_code == 200
    by_id = {s["id"]: s for s in resp.json()["subtasks"]}
    assert by_id["s1"]["completed"] is True
    assert by_id["s2"]["completed"] is False


# ── Log append-only ────────────────────────────────────────────────────────────

async def test_no_patch_log_route(async_client: AsyncClient, auth_headers: dict):
    from uuid import uuid4
    resp = await async_client.patch(f"/logs/{uuid4()}", json={}, headers=auth_headers)
    assert resp.status_code in (404, 405)


async def test_no_delete_log_route(async_client: AsyncClient, auth_headers: dict):
    from uuid import uuid4
    resp = await async_client.delete(f"/logs/{uuid4()}", headers=auth_headers)
    assert resp.status_code in (404, 405)


async def test_created_log_appears_in_list(
    async_client: AsyncClient, auth_headers: dict, seeded_data: dict
):
    pid = seeded_data["project"].id
    create = await async_client.post(
        f"/projects/{pid}/logs",
        json={"skill": "orc-test", "outcome": "success", "summary": "All passed"},
        headers=auth_headers,
    )
    assert create.status_code == 201
    log_id = create.json()["id"]

    resp = await async_client.get(f"/projects/{pid}/logs", headers=auth_headers)
    assert resp.status_code == 200
    ids = [l["id"] for l in resp.json()]
    assert log_id in ids
