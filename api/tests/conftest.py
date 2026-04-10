import os
import subprocess
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Must be set before any app imports — app/core/db.py creates the engine at import time
TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://localhost/taskorc_test",
)
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from app.core.auth import generate_pat, hash_pat  # noqa: E402
from app.core.db import get_db  # noqa: E402
from app.models.user import User  # noqa: E402
from app.schemas.note import NoteCategory, NoteCreate  # noqa: E402
from app.schemas.project import ProjectCreate  # noqa: E402
from app.schemas.task import TaskCreate, TaskStatus  # noqa: E402
from app.services import note as note_service  # noqa: E402
from app.services import project as project_service  # noqa: E402
from app.services import task as task_service  # noqa: E402
from main import app  # noqa: E402

_API_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

_TABLES = [
    "artifacts", "logs", "notes", "tasks", "projects", "users",
]


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    result = subprocess.run(
        ["uv", "run", "alembic", "upgrade", "head"],
        cwd=_API_DIR,
        env={**os.environ, "DATABASE_URL": TEST_DATABASE_URL},
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Alembic migration failed:\n{result.stderr}")


_test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
_TestSession = async_sessionmaker(_test_engine, expire_on_commit=False)


@pytest_asyncio.fixture(autouse=True)
async def truncate_tables():
    """Wipe all tables before each test for a clean slate."""
    async with _test_engine.connect() as conn:
        await conn.execute(
            text(f"TRUNCATE TABLE {', '.join(_TABLES)} RESTART IDENTITY CASCADE")
        )
        await conn.commit()


@pytest_asyncio.fixture
async def db_session():
    async with _TestSession() as session:
        yield session


@pytest_asyncio.fixture
async def async_client(db_session: AsyncSession):
    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            yield client
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest_asyncio.fixture
async def auth_user(db_session: AsyncSession):
    """Creates a test user in the DB and returns (user, raw_pat)."""
    pat = generate_pat()
    user = User(
        name="Test User",
        email=f"test-{uuid4()}@example.com",
        pat_hash=hash_pat(pat),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user, pat


@pytest_asyncio.fixture
async def auth_headers(auth_user):
    """Returns Authorization header dict for the test user."""
    _user, pat = auth_user
    return {"Authorization": f"Bearer {pat}"}


@pytest_asyncio.fixture
async def seeded_data(db_session: AsyncSession, auth_user):
    """Creates one Project, one Task (planned), and one Note for the test user."""
    user, pat = auth_user

    project = await project_service.create_project(
        db_session, user.id, ProjectCreate(name="Test Project")
    )
    task = await task_service.create_task(
        db_session,
        project.id,
        user.id,
        TaskCreate(title="Test Task", status=TaskStatus.planned, priority=5),
    )
    note = await note_service.create_note(
        db_session,
        project.id,
        user.id,
        NoteCreate(title="Test Note", body="Test body", category=NoteCategory.general),
    )
    return {"project": project, "task": task, "note": note, "user": user, "pat": pat}
