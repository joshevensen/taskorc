---
status: complete
priority: 1
---

# 1 — Project Scaffolding

## Description

Set up the foundational structure of the API before writing any domain code. This phase installs all dependencies, creates the directory layout, wires up configuration via environment variables, establishes the async database session, and creates the `.env` files. Every subsequent phase builds directly on this.

## Acceptance Criteria

- [x] All dependencies are declared in `pyproject.toml` and installable via `uv sync`
- [x] The `app/` directory structure exists with `core/`, `models/`, `schemas/`, `routers/`, `services/` subdirectories
- [x] `app/core/config.py` loads all required env vars via `pydantic-settings` and raises a clear error on startup if any are missing
- [x] `app/core/db.py` exports an async SQLAlchemy engine and a `get_db` dependency that yields an `AsyncSession`
- [x] `main.py` creates the FastAPI app instance and is importable without error
- [x] `.env.example` documents every required env var with a description comment
- [x] `.env` is present locally and gitignored
- [x] `uv run fastapi dev` starts the server without errors

## Subtasks

### 1 — Install dependencies

Add all required packages to `pyproject.toml` and run `uv sync`.

**Prompt:** Add the following dependencies to `api/pyproject.toml` under `[project] dependencies`: `sqlalchemy[asyncio]`, `alembic`, `asyncpg`, `passlib[bcrypt]`, `python-dotenv`, `pydantic-settings`. Run `uv sync` to install them. Confirm the lock file updates cleanly.

---

### 2 — Create directory structure

Scaffold the `app/` package and all subdirectories with `__init__.py` files.

**Prompt:** Inside `api/`, create the following directory and file structure. Each directory needs an empty `__init__.py` to be a Python package:
```
app/__init__.py
app/core/__init__.py
app/models/__init__.py
app/schemas/__init__.py
app/routers/__init__.py
app/services/__init__.py
tests/__init__.py
```
Do not add any logic yet — just the empty files.

---

### 3 — Config / settings

Create `app/core/config.py` that loads env vars and exposes a `settings` singleton.

**Prompt:** Create `api/app/core/config.py` using `pydantic-settings`. Define a `Settings` class with the following fields: `DATABASE_URL` (str), `CORS_ORIGINS` (str, default `"http://localhost"`). Instantiate `settings = Settings()` at module level. FastAPI will fail fast on startup if any required var is missing.

---

### 4 — Database session

Create the async SQLAlchemy engine and session dependency.

**Prompt:** Create `api/app/core/db.py`. Use `sqlalchemy.ext.asyncio` to create an `AsyncEngine` from `settings.DATABASE_URL`. Create an `AsyncSessionLocal` using `async_sessionmaker`. Define a `get_db` async generator dependency that yields an `AsyncSession` and closes it after the request. Export `engine`, `AsyncSessionLocal`, and `get_db`.

---

### 5 — Environment files

Create `.env.example` and local `.env`.

**Prompt:** Create `api/.env.example` with all required environment variables, each with a descriptive comment:
```
# PostgreSQL connection string
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/taskorc

# Comma-separated list of allowed CORS origins
CORS_ORIGINS=http://localhost
```
Then create `api/.env` (gitignored) with real local values filled in. Confirm `api/.gitignore` exists and includes `.env`.

---

### 6 — App factory

Update `main.py` to use the app structure.

**Prompt:** Update `api/main.py` to import `settings` from `app.core.config` and create the FastAPI app with a `title` of `"TaskOrc API"` and `version` of `"0.1.0"`. Add a `/health` GET endpoint that returns `{"status": "ok"}`. The root `Hello World` endpoint can be removed. Confirm `uv run fastapi dev` starts without errors and `/health` returns 200.

---

### 7 — Commit and push

**Prompt:** From the repo root, stage and commit all changes from this phase, then push:
```bash
git add api/pyproject.toml api/uv.lock api/main.py api/app/ api/tests/ api/.env.example api/.gitignore
git commit -m "feat(api): phase 1 — project scaffolding"
git push
```
