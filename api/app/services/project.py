from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services.ownership import assert_project_owner


async def create_project(db: AsyncSession, user_id: UUID, data: ProjectCreate) -> Project:
    project = Project(user_id=user_id, **data.model_dump())
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


async def list_projects(db: AsyncSession, user_id: UUID) -> list[Project]:
    result = await db.execute(select(Project).where(Project.user_id == user_id))
    return list(result.scalars().all())


async def get_project(db: AsyncSession, project_id: UUID, user_id: UUID) -> Project:
    return await assert_project_owner(db, project_id, user_id)


async def update_project(db: AsyncSession, project_id: UUID, user_id: UUID, data: ProjectUpdate) -> Project:
    project = await assert_project_owner(db, project_id, user_id)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(project, field, value)
    await db.commit()
    await db.refresh(project)
    return project
