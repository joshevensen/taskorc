---
status: complete
priority: 3
---

# 3 — Migrations

## Description

Initialize Alembic and generate the first migration from the ORM models defined in task 2. Apply the migration to the local PostgreSQL database. This task has no new Python logic — it is purely about getting the schema into the database correctly.

## Acceptance Criteria

- [x] Alembic is initialized and `alembic/env.py` uses the async engine from `app/core/db.py`
- [x] `alembic/env.py` imports all models from `app/models` so autogenerate detects them
- [x] `alembic revision --autogenerate` produces a migration file with all six tables
- [x] The migration includes `CREATE TYPE` statements for all PostgreSQL enums before the tables that use them
- [x] `alembic upgrade head` applies cleanly against a fresh local database with no errors
- [x] `alembic downgrade base` reverses the migration cleanly (tables and enum types dropped)
- [x] `alembic current` reports the migration as applied after upgrade

## Subtasks

### 1 — Initialize Alembic

**Prompt:** From the `api/` directory, run `alembic init alembic`. This creates `alembic/` and `alembic.ini`. Update `alembic.ini` to set `sqlalchemy.url` to a placeholder (it will be overridden in `env.py` from settings — do not hardcode the URL). Add `alembic/` to `.gitignore` exclusions only for `__pycache__` — the migration files themselves must be committed.

---

### 2 — Configure env.py for async

**Prompt:** Rewrite `api/alembic/env.py` to support async SQLAlchemy. The key changes from the default:
1. Import `asyncio` and use `asyncio.run()` to wrap the migration runner
2. Import `engine` from `app.core.db` and use it instead of creating a new engine from `alembic.ini`
3. Import `Base` from `app.models.base` and set `target_metadata = Base.metadata`
4. Import all models (`from app.models import User, Project, Task, Note, Log, Artifact`) so autogenerate can see them
5. Use `AsyncConnection.run_sync(do_run_migrations)` pattern for the actual migration execution

Follow the SQLAlchemy async Alembic pattern from the official docs.

---

### 3 — Generate first migration

**Prompt:** From `api/`, run `alembic revision --autogenerate -m "initial schema"`. Open the generated migration file and verify:
- All six tables are present: `users`, `projects`, `tasks`, `notes`, `logs`, `artifacts`
- All PostgreSQL enum `CREATE TYPE` statements appear before the tables that use them
- UUID columns use `gen_random_uuid()` as server default
- Foreign keys have correct `ondelete` rules (CASCADE for most, SET NULL for `logs.task_id`)
- JSONB columns are typed as JSONB (not JSON)

Fix any missing or incorrect items manually in the migration file before proceeding.

---

### 4 — Apply migration

**Prompt:** Ensure a local PostgreSQL database named `taskorc` exists (create it if needed with `createdb taskorc`). From `api/`, run `alembic upgrade head`. Confirm it completes with no errors. Then connect to the database and verify all six tables exist with the correct columns. Run `alembic current` and confirm it shows the migration as applied at `head`.

---

### 5 — Verify downgrade

**Prompt:** Run `alembic downgrade base` and confirm it reverses cleanly — all tables are dropped and all enum types are removed. Then run `alembic upgrade head` again to restore the schema. A clean downgrade proves the migration is reversible and the enum drop order is correct.
