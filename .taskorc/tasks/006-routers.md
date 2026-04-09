---
status: complete
priority: 6
---

# 6 — Routers & Services

## Description

Implement all API endpoints. One router + one service file per entity. The router handles HTTP concerns (request parsing, response serialization, auth dependency injection). The service handles all database logic. Routers must not contain raw SQLAlchemy queries — that belongs in services.

## Acceptance Criteria

- [x] All endpoints from the CLI Commands doc are implemented and return the correct HTTP status codes
- [x] Every router injects `get_current_user` via `Depends` — no unprotected endpoints except `/auth/*` and `/health`
- [x] Routers return Pydantic response schemas — no raw ORM objects in responses
- [x] Services use `AsyncSession` and `await` all DB calls
- [x] `GET /projects/{project_id}/tasks/next` returns the lowest `priority` value among `planned` tasks, or 404 if none
- [x] `PUT /tasks/{id}/subtasks` replaces the entire subtasks array atomically
- [x] `POST /tasks/{id}/subtasks/{subtask_id}/complete` sets the matching subtask's `completed` to `true` within the JSONB array
- [x] `POST /projects/{project_id}/logs` creates a log — no update or delete endpoints exist for logs
- [x] All routers are registered in `main.py` with appropriate prefixes and tags
- [x] FastAPI's auto-generated `/docs` shows all endpoints correctly

## Subtasks

### 1 — User router & service

**Prompt:** Create `api/app/services/user.py` and `api/app/routers/user.py`.

Service functions:
- `get_user(db, user_id) -> User`
- `update_user(db, user_id, data: UserUpdateRequest) -> User` — partial update, only set non-None fields

Router endpoints (all require `get_current_user`):
- `GET /users/me` → `UserResponse`
- `PATCH /users/me` → `UserResponse`

Register with prefix `/users`, tag `users`.

---

### 2 — Projects router & service

**Prompt:** Create `api/app/services/project.py` and `api/app/routers/project.py`.

Service functions:
- `create_project(db, user_id, data: ProjectCreate) -> Project`
- `list_projects(db, user_id) -> list[Project]`
- `get_project(db, project_id) -> Project`
- `update_project(db, project_id, data: ProjectUpdate) -> Project`

Router endpoints (all require `get_current_user`):
- `POST /projects` → `ProjectResponse` (201)
- `GET /projects` → `list[ProjectResponse]`
- `GET /projects/{id}` → `ProjectResponse`
- `PATCH /projects/{id}` → `ProjectResponse`

Register with prefix `/projects`, tag `projects`.

---

### 3 — Tasks router & service

**Prompt:** Create `api/app/services/task.py` and `api/app/routers/task.py`.

Service functions:
- `create_task(db, project_id, data: TaskCreate) -> Task`
- `list_tasks(db, project_id, status=None, limit=None) -> list[Task]`
- `get_task(db, task_id) -> Task`
- `update_task(db, task_id, data: TaskUpdate) -> Task`
- `set_subtasks(db, task_id, subtasks: list[SubtaskItem]) -> Task` — replaces subtasks array
- `complete_subtask(db, task_id, subtask_id: str) -> Task` — sets `completed=true` on matching subtask in JSONB
- `next_task(db, project_id) -> Task | None` — lowest priority integer among `planned` tasks

Router endpoints:
- `POST /projects/{project_id}/tasks` → `TaskResponse` (201)
- `GET /projects/{project_id}/tasks` → `list[TaskResponse]` (query params: `status`, `limit`)
- `GET /tasks/{id}` → `TaskResponse`
- `PATCH /tasks/{id}` → `TaskResponse`
- `PUT /tasks/{id}/subtasks` → `TaskResponse`
- `POST /tasks/{id}/subtasks/{subtask_id}/complete` → `TaskResponse`
- `GET /projects/{project_id}/tasks/next` → `TaskResponse` or 404

Register with tag `tasks`. Task routes split across two prefixes — `/projects` and `/tasks` — register both on the same router.

---

### 4 — Notes router & service

**Prompt:** Create `api/app/services/note.py` and `api/app/routers/note.py`.

Service functions:
- `create_note(db, project_id, data: NoteCreate) -> Note`
- `list_notes(db, project_id, category=None, limit=None) -> list[Note]`
- `get_note(db, note_id) -> Note`
- `update_note(db, note_id, data: NoteUpdate) -> Note`
- `delete_note(db, note_id) -> None`

Router endpoints:
- `POST /projects/{project_id}/notes` → `NoteResponse` (201)
- `GET /projects/{project_id}/notes` → `list[NoteResponse]` (query params: `category`, `limit`)
- `GET /notes/{id}` → `NoteResponse`
- `PATCH /notes/{id}` → `NoteResponse`
- `DELETE /notes/{id}` → 204 No Content

Register with tag `notes`.

---

### 5 — Logs router & service

**Prompt:** Create `api/app/services/log.py` and `api/app/routers/log.py`.

Service functions:
- `create_log(db, project_id, data: LogCreate) -> Log`
- `list_logs(db, project_id, skill=None, task_id=None, limit=None) -> list[Log]`

No update or delete service functions — logs are append-only.

Router endpoints:
- `POST /projects/{project_id}/logs` → `LogResponse` (201)
- `GET /projects/{project_id}/logs` → `list[LogResponse]` (query params: `skill`, `task_id`, `limit`)

Register with tag `logs`.

---

### 6 — Artifacts router & service

**Prompt:** Create `api/app/services/artifact.py` and `api/app/routers/artifact.py`.

Service functions:
- `create_artifact(db, user_id, data: ArtifactCreate) -> Artifact`
- `list_artifacts(db, parent_type, parent_id) -> list[Artifact]`
- `get_artifact(db, artifact_id) -> Artifact`
- `update_artifact(db, artifact_id, data: ArtifactUpdate) -> Artifact`

Router endpoints:
- `POST /artifacts` → `ArtifactResponse` (201)
- `GET /artifacts` → `list[ArtifactResponse]` (query params: `parent_type`, `parent_id`)
- `GET /artifacts/{id}` → `ArtifactResponse`
- `PATCH /artifacts/{id}` → `ArtifactResponse`

Register with prefix `/artifacts`, tag `artifacts`.

---

### 7 — Register all routers

**Prompt:** Update `api/main.py` to import and register all six routers with their prefixes and tags. Start the dev server and open `/docs`. Verify every endpoint appears, all request bodies show the correct schema, and all response schemas are documented. Fix any missing imports or registration issues.
