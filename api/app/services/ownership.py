from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project


async def assert_project_owner(db: AsyncSession, project_id: UUID, user_id: UUID) -> Project:
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    # Always 403 — never reveal whether the resource exists
    if project is None or project.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return project
