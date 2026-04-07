---
status: planned
priority: 2
---

# 2 — ORM Models

## Description

Define all six SQLAlchemy models in Python. Alembic will generate the database schema from these in Phase 3 — getting the models right here determines the correctness of the entire schema. Focus on accurate column types, relationships, and constraints. No migrations yet.

## Acceptance Criteria

- [ ] `app/models/base.py` defines a `DeclarativeBase` with `id` (UUID, default generated), `created_at`, and `updated_at` columns shared across all models
- [ ] All six models are defined: `User`, `Project`, `Task`, `Note`, `Log`, `Artifact`
- [ ] JSONB columns are used for `settings`, `tech_stack`, `subtasks`, `acceptance_criteria`, and `metadata`
- [ ] PostgreSQL enums are defined for `Task.status`, `Task.execution_mode`, `Note.category`, `Log.outcome`, `Artifact.type`, and `Artifact.parent_type`
- [ ] All foreign keys are declared with appropriate `ondelete` behaviour
- [ ] SQLAlchemy `relationship()` declarations exist for all associations
- [ ] All models are imported in `app/models/__init__.py` so Alembic can discover them
- [ ] `from app.models import User, Project, Task, Note, Log, Artifact` works without error

## Subtasks

### 2.1 — Base model

Create the declarative base with shared columns.

**Prompt:** Create `api/app/models/base.py`. Define a `Base` class using `sqlalchemy.orm.DeclarativeBase`. Add a mixin `TimestampMixin` with: `id` (UUID primary key, server default `gen_random_uuid()`), `created_at` (DateTime with timezone, server default `now()`, not nullable), `updated_at` (DateTime with timezone, server default `now()`, `onupdate=func.now()`, not nullable). All models will inherit from `Base` and include `TimestampMixin`.

---

### 2.2 — User model

**Prompt:** Create `api/app/models/user.py`. Define `User(Base, TimestampMixin)` with table name `users` and columns: `name` (String, not nullable), `email` (String, unique, not nullable, indexed), `pat_hash` (Text, nullable — stores bcrypt hash of the active PAT), `settings` (JSONB, nullable, default `{}`), `founder_notes` (Text, nullable). Add a `relationship("Project", back_populates="user", cascade="all, delete-orphan")`. Email must have a unique constraint.

---

### 2.3 — Project model

**Prompt:** Create `api/app/models/project.py`. Define `Project(Base, TimestampMixin)` with table name `projects` and columns: `user_id` (UUID FK → `users.id`, ondelete CASCADE, not nullable), `name` (String, not nullable), `description` (Text, nullable), `repo_url` (String, nullable), `tech_stack` (JSONB, nullable, default `[]`), `branch_prefix` (String, nullable), `base_branch` (String, nullable, default `"main"`), `test_command` (String, nullable), `lint_command` (String, nullable), `format_command` (String, nullable). Add relationships to `User`, `Task`, `Note`, `Log`, `Artifact` with appropriate `back_populates` and `cascade="all, delete-orphan"`.

---

### 2.4 — Task model

**Prompt:** Create `api/app/models/task.py`. Define PostgreSQL enums using `sqlalchemy.dialects.postgresql.ENUM`:
- `task_status`: `draft`, `planned`, `in_progress`, `complete`, `failed`, `on_hold`, `cancelled`
- `execution_mode`: `guided`, `autonomous`

Define `Task(Base, TimestampMixin)` with table name `tasks` and columns: `project_id` (UUID FK → `projects.id`, ondelete CASCADE, not nullable), `title` (String, not nullable), `description` (Text, nullable), `problem` (Text, nullable), `acceptance_criteria` (JSONB, nullable), `priority` (Integer, nullable), `status` (task_status enum, not nullable, default `draft`), `subtasks` (JSONB, not nullable, default `[]`), `branch` (String, nullable), `pr_url` (String, nullable), `execution_mode` (execution_mode enum, nullable). Add relationship to `Project`, `Log`, `Artifact`.

---

### 2.5 — Note model

**Prompt:** Create `api/app/models/note.py`. Define a `note_category` PostgreSQL enum: `product`, `strategy`, `users`, `market`, `decisions`, `constraints`, `goals`, `general`. Define `Note(Base, TimestampMixin)` with table name `notes` and columns: `project_id` (UUID FK → `projects.id`, ondelete CASCADE, not nullable), `title` (String, not nullable), `body` (Text, not nullable), `category` (note_category enum, not nullable). Add relationship to `Project`.

---

### 2.6 — Log model

**Prompt:** Create `api/app/models/log.py`. Define a `log_outcome` PostgreSQL enum: `success`, `failure`, `skipped`. Define `Log(Base, TimestampMixin)` with table name `logs` and columns: `project_id` (UUID FK → `projects.id`, ondelete CASCADE, not nullable), `task_id` (UUID FK → `tasks.id`, ondelete SET NULL, nullable), `skill` (String, not nullable), `duration` (Integer, nullable, in milliseconds), `outcome` (log_outcome enum, not nullable), `summary` (Text, nullable), `metadata` (JSONB, nullable). Logs must never be updated or deleted — enforce at the service layer, not the DB layer. Add relationships to `Project` and `Task`.

---

### 2.7 — Artifact model

**Prompt:** Create `api/app/models/artifact.py`. Define PostgreSQL enums:
- `artifact_type`: `figma`, `video`, `document`, `error_log`, `screenshot`, `other`
- `artifact_parent_type`: `project`, `task`

Define `Artifact(Base, TimestampMixin)` with table name `artifacts` and columns: `user_id` (UUID FK → `users.id`, ondelete CASCADE, not nullable), `title` (String, not nullable), `url` (String, not nullable), `body` (Text, nullable), `type` (artifact_type enum, not nullable), `parent_type` (artifact_parent_type enum, not nullable), `parent_id` (UUID, not nullable). No FK constraint on `parent_id` — polymorphic reference resolved at the service layer. Add relationship to `User`.

---

### 2.8 — Wire models into package

**Prompt:** Update `api/app/models/__init__.py` to import all models: `from .user import User`, `from .project import Project`, `from .task import Task`, `from .note import Note`, `from .log import Log`, `from .artifact import Artifact`. This ensures Alembic's autogenerate sees all models when it imports the package. Confirm `from app.models import User, Project, Task, Note, Log, Artifact` works from the `api/` directory.

---

### 2.9 — Commit and push

**Prompt:** From the repo root, stage and commit all changes from this phase, then push:
```bash
git add api/app/models/
git commit -m "feat(api): phase 2 — ORM models"
git push
```
