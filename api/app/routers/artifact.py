from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db import get_db
from app.models.user import User
from app.schemas.artifact import ArtifactCreate, ArtifactParentType, ArtifactResponse, ArtifactUpdate
from app.services import artifact as artifact_service

router = APIRouter(prefix="/artifacts", tags=["artifacts"])


@router.post("", response_model=ArtifactResponse, status_code=status.HTTP_201_CREATED)
async def create_artifact(
    data: ArtifactCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await artifact_service.create_artifact(db, current_user.id, data)


@router.get("", response_model=list[ArtifactResponse])
async def list_artifacts(
    parent_type: ArtifactParentType,
    parent_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await artifact_service.list_artifacts(db, parent_type, parent_id, current_user.id)


@router.get("/{id}", response_model=ArtifactResponse)
async def get_artifact(
    id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await artifact_service.get_artifact(db, id, current_user.id)


@router.patch("/{id}", response_model=ArtifactResponse)
async def update_artifact(
    id: UUID,
    data: ArtifactUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await artifact_service.update_artifact(db, id, current_user.id, data)
