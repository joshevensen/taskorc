---
status: complete
priority: 5
---

# 5 — Pydantic Schemas

## Description

Define all Pydantic v2 request and response schemas. These are the API's contract — what the CLI sends in and what comes back. Keep request and response schemas separate. Schemas must match the entity definitions exactly, including enum values, nullable fields, and JSONB shapes.

## Acceptance Criteria

- [x] One schema file per entity in `app/schemas/`
- [x] Every entity has distinct `Create`, `Update`, and `Response` schemas where applicable
- [x] `Update` schemas use `Optional` fields with `None` defaults (partial update pattern)
- [x] `Response` schemas include `id`, `created_at`, `updated_at` from the base model
- [x] Enum values in schemas match the PostgreSQL enum values exactly
- [x] JSONB fields are typed precisely: `subtasks` is `list[SubtaskItem]`, `acceptance_criteria` is `list[str] | None`, `tech_stack` is `list[str]`, `settings` is `dict[str, Any]`, `metadata` is `dict[str, Any] | None`
- [x] `SubtaskItem` schema has `id`, `description`, `prompt`, `completed` fields
- [x] All schemas are importable from `app/schemas/__init__.py`

## Subtasks

### 1 — Shared / base schemas

**Prompt:** Create `api/app/schemas/base.py`. Define a `BaseResponse` schema with `id: UUID`, `created_at: datetime`, `updated_at: datetime`. All `*Response` schemas will inherit from this. Configure `model_config = ConfigDict(from_attributes=True)` on `BaseResponse` so SQLAlchemy ORM objects can be passed directly to `model_validate`.

---

### 2 — User schemas

**Prompt:** Create `api/app/schemas/user.py` with:

`UserResponse(BaseResponse)` — fields: `name: str`, `email: str`, `settings: dict[str, Any]`, `founder_notes: str | None`

`UserUpdateRequest` — fields: `founder_notes: str | None = None`, `settings: dict[str, Any] | None = None`. Both optional — partial update.

---

### 3 — Project schemas

**Prompt:** Create `api/app/schemas/project.py` with:

`ProjectCreate` — fields: `name: str`, `description: str | None = None`, `repo_url: str | None = None`, `tech_stack: list[str] = []`, `branch_prefix: str | None = None`, `base_branch: str = "main"`, `test_command: str | None = None`, `lint_command: str | None = None`, `format_command: str | None = None`

`ProjectUpdate` — all fields from `ProjectCreate` but all optional with `None` defaults.

`ProjectResponse(BaseResponse)` — all fields from `ProjectCreate` plus `user_id: UUID`.

---

### 4 — Task schemas

**Prompt:** Create `api/app/schemas/task.py` with:

`SubtaskItem` — fields: `id: str`, `description: str`, `prompt: str`, `completed: bool = False`

`TaskCreate` — fields: `title: str`, `description: str | None = None`, `problem: str | None = None`, `acceptance_criteria: list[str] | None = None`, `priority: int | None = None`, `status: TaskStatus = TaskStatus.draft`

`TaskUpdate` — all fields from `TaskCreate` optional, plus: `branch: str | None = None`, `pr_url: str | None = None`, `execution_mode: ExecutionMode | None = None`

`TaskResponse(BaseResponse)` — all fields plus `project_id: UUID`, `subtasks: list[SubtaskItem]`

Define `TaskStatus` and `ExecutionMode` as Python `enum.Enum` classes in this file, values matching the PostgreSQL enums exactly.

---

### 5 — Note schemas

**Prompt:** Create `api/app/schemas/note.py` with:

`NoteCreate` — fields: `title: str`, `body: str`, `category: NoteCategory`

`NoteUpdate` — all fields optional with `None` defaults.

`NoteResponse(BaseResponse)` — all fields plus `project_id: UUID`

Define `NoteCategory` as a Python enum matching the PostgreSQL enum values: `product`, `strategy`, `users`, `market`, `decisions`, `constraints`, `goals`, `general`.

---

### 6 — Log schemas

**Prompt:** Create `api/app/schemas/log.py` with:

`LogCreate` — fields: `skill: str`, `task_id: UUID | None = None`, `duration: int | None = None`, `outcome: LogOutcome`, `summary: str | None = None`, `metadata: dict[str, Any] | None = None`

`LogResponse(BaseResponse)` — all fields plus `project_id: UUID`

Define `LogOutcome` enum: `success`, `failure`, `skipped`. No `LogUpdate` — logs are append-only.

---

### 7 — Artifact schemas

**Prompt:** Create `api/app/schemas/artifact.py` with:

`ArtifactCreate` — fields: `title: str`, `url: str`, `body: str | None = None`, `type: ArtifactType`, `parent_type: ArtifactParentType`, `parent_id: UUID`

`ArtifactUpdate` — fields: `title: str | None = None`, `body: str | None = None`

`ArtifactResponse(BaseResponse)` — all fields plus `user_id: UUID`

Define `ArtifactType` enum: `figma`, `video`, `document`, `error_log`, `screenshot`, `other`. Define `ArtifactParentType` enum: `project`, `task`.

---

### 8 — Wire schemas into package

**Prompt:** Update `api/app/schemas/__init__.py` to import and re-export all schemas and enums. Confirm `from app.schemas import TaskCreate, TaskResponse, SubtaskItem, NoteCategory, LogOutcome` and all other schemas are importable without error.
