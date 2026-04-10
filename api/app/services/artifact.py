from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.artifact import Artifact
from app.models.task import Task
from app.schemas.artifact import ArtifactCreate, ArtifactParentType, ArtifactUpdate
from app.services.ownership import assert_project_owner


async def _assert_artifact_owner(db: AsyncSession, artifact: Artifact, user_id: UUID) -> None:
    """Resolve artifact ownership by traversing to the parent project."""
    if artifact.parent_type == ArtifactParentType.project.value:
        await assert_project_owner(db, artifact.parent_id, user_id)
    else:
        # parent_type == "task" — traverse to the task's project
        result = await db.execute(select(Task).where(Task.id == artifact.parent_id))
        task = result.scalar_one_or_none()
        if task is None:
            raise HTTPException(status_code=403, detail="Forbidden")
        await assert_project_owner(db, task.project_id, user_id)


async def create_artifact(db: AsyncSession, user_id: UUID, data: ArtifactCreate) -> Artifact:
    # Verify ownership of the parent before creating
    if data.parent_type == ArtifactParentType.project:
        await assert_project_owner(db, data.parent_id, user_id)
    else:
        result = await db.execute(select(Task).where(Task.id == data.parent_id))
        task = result.scalar_one_or_none()
        if task is None:
            raise HTTPException(status_code=403, detail="Forbidden")
        await assert_project_owner(db, task.project_id, user_id)

    artifact = Artifact(user_id=user_id, **data.model_dump())
    db.add(artifact)
    await db.commit()
    await db.refresh(artifact)
    return artifact


async def list_artifacts(
    db: AsyncSession,
    parent_type: ArtifactParentType,
    parent_id: UUID,
    user_id: UUID,
) -> list[Artifact]:
    # Verify ownership of the parent before listing
    if parent_type == ArtifactParentType.project:
        await assert_project_owner(db, parent_id, user_id)
    else:
        result = await db.execute(select(Task).where(Task.id == parent_id))
        task = result.scalar_one_or_none()
        if task is None:
            raise HTTPException(status_code=403, detail="Forbidden")
        await assert_project_owner(db, task.project_id, user_id)

    result = await db.execute(
        select(Artifact)
        .where(Artifact.parent_type == parent_type.value)
        .where(Artifact.parent_id == parent_id)
    )
    return list(result.scalars().all())


async def get_artifact(db: AsyncSession, artifact_id: UUID, user_id: UUID) -> Artifact:
    result = await db.execute(select(Artifact).where(Artifact.id == artifact_id))
    artifact = result.scalar_one_or_none()
    if artifact is None:
        raise HTTPException(status_code=404, detail="Artifact not found")
    await _assert_artifact_owner(db, artifact, user_id)
    return artifact


async def update_artifact(db: AsyncSession, artifact_id: UUID, user_id: UUID, data: ArtifactUpdate) -> Artifact:
    artifact = await get_artifact(db, artifact_id, user_id)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(artifact, field, value)
    await db.commit()
    await db.refresh(artifact)
    return artifact
