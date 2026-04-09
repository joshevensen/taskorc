from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.artifact import Artifact
from app.schemas.artifact import ArtifactCreate, ArtifactParentType, ArtifactUpdate


async def create_artifact(db: AsyncSession, user_id: UUID, data: ArtifactCreate) -> Artifact:
    artifact = Artifact(user_id=user_id, **data.model_dump())
    db.add(artifact)
    await db.commit()
    await db.refresh(artifact)
    return artifact


async def list_artifacts(
    db: AsyncSession,
    parent_type: ArtifactParentType,
    parent_id: UUID,
) -> list[Artifact]:
    result = await db.execute(
        select(Artifact)
        .where(Artifact.parent_type == parent_type.value)
        .where(Artifact.parent_id == parent_id)
    )
    return list(result.scalars().all())


async def get_artifact(db: AsyncSession, artifact_id: UUID) -> Artifact:
    result = await db.execute(select(Artifact).where(Artifact.id == artifact_id))
    artifact = result.scalar_one_or_none()
    if artifact is None:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return artifact


async def update_artifact(db: AsyncSession, artifact_id: UUID, data: ArtifactUpdate) -> Artifact:
    artifact = await get_artifact(db, artifact_id)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(artifact, field, value)
    await db.commit()
    await db.refresh(artifact)
    return artifact
