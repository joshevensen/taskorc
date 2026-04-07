---
status: planned
priority: 8
---

# 8 — Testing

## Description

Write automated tests covering auth, CRUD, authorization, and business logic. Tests use a real PostgreSQL test database — not mocks or SQLite. The goal is confidence that the API works end-to-end before hardening.

## Acceptance Criteria

- [ ] `pytest` runs from `api/` with no configuration beyond setting `TEST_DATABASE_URL`
- [ ] Fixtures provide: an async test client, a test database session, an authenticated user, and common seeded data (one project, one task, one note)
- [ ] Auth tests cover: PAT generation, valid token acceptance, invalid token rejection, revocation
- [ ] CRUD tests cover at least one happy-path test per endpoint (create, read, update, delete where applicable)
- [ ] Authorization tests verify a second user cannot access the first user's resources (returns 403)
- [ ] Business logic tests cover: `task/next` returns lowest priority planned task, subtask completion marks correct subtask, log endpoints have no update/delete routes
- [ ] All tests pass against a clean test database with migrations applied
- [ ] No test modifies the development database

## Subtasks

### 1 — Test setup and fixtures

**Prompt:** Create `api/tests/conftest.py`. Set up:

1. A `TEST_DATABASE_URL` env var pointing to a separate test database (e.g., `taskorc_test`). Apply migrations to it before tests run using `alembic upgrade head` programmatically or via a pytest session fixture.

2. An `async_client` fixture using `httpx.AsyncClient` with `ASGITransport(app=app)` and `base_url="http://test"`.

3. A `db_session` fixture that provides an `AsyncSession` connected to the test database, rolling back after each test.

4. An `auth_headers` fixture that creates a test user directly in the DB, generates a PAT, and returns `{"Authorization": "Bearer <pat>"}` — bypass the `POST /auth/token` endpoint for test setup speed.

5. A `seeded_data` fixture that creates one Project, one Task (status=planned), and one Note using the service layer, returning them for use in tests.

---

### 2 — Auth tests

**Prompt:** Create `api/tests/test_auth.py`. Test:

- `POST /auth/token` with name and email returns 200 with a token prefixed `orc_`
- `GET /users/me` with the returned token returns 200
- `GET /users/me` with a tampered token returns 401
- `GET /users/me` with no Authorization header returns 401
- `DELETE /auth/token` with a valid token returns 200
- `GET /users/me` with the revoked token returns 401

---

### 3 — CRUD tests

**Prompt:** Create `api/tests/test_crud.py`. Write at least one happy-path test per endpoint group using the `auth_headers` and `seeded_data` fixtures:

- **User:** GET `/users/me`, PATCH `/users/me`
- **Projects:** POST, GET list, GET single, PATCH
- **Tasks:** POST, GET list, GET single, PATCH, PUT subtasks, POST subtask complete
- **Notes:** POST, GET list, GET single, PATCH, DELETE
- **Logs:** POST, GET list
- **Artifacts:** POST, GET list, GET single, PATCH

Verify correct status codes (200, 201, 204) and that response bodies match the expected schemas.

---

### 4 — Authorization tests

**Prompt:** Create `api/tests/test_authz.py`. Create two users (user A and user B) with separate auth headers. Seed data under user A. Verify user B receives 403 on:

- `GET /projects/{user_a_project_id}`
- `PATCH /projects/{user_a_project_id}`
- `GET /tasks/{user_a_task_id}`
- `PATCH /tasks/{user_a_task_id}`
- `GET /notes/{user_a_note_id}`
- `DELETE /notes/{user_a_note_id}`
- `GET /projects/{user_a_project_id}/logs`
- `POST /projects/{user_a_project_id}/logs`

---

### 5 — Business logic tests

**Prompt:** Create `api/tests/test_business_logic.py`. Test:

**Task priority ordering:** Create three planned tasks with priorities 10, 1, and 5. Call `GET /projects/{id}/tasks/next`. Verify the task with priority 1 is returned. Verify tasks with `draft` status are excluded from `/next` even if they have lower priority numbers.

**Subtask completion:** Create a task with two subtasks. POST to complete the first subtask. GET the task and verify only the first subtask has `completed=true`.

**Log append-only:** Verify no `PATCH /logs/{id}` or `DELETE /logs/{id}` routes exist (expect 405 or 404). Verify a created log is returned in `GET /projects/{id}/logs`.

---

### 6 — Commit and push

**Prompt:** From the repo root, stage and commit all changes from this phase, then push:
```bash
git add api/tests/
git commit -m "test(api): phase 8 — auth, CRUD, authz, and business logic tests"
git push
```
