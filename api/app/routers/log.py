from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db import get_db
from app.models.user import User
from app.schemas.log import LogCreate, LogResponse
from app.services import log as log_service

router = APIRouter(tags=["logs"])


@router.post("/projects/{project_id}/logs", response_model=LogResponse, status_code=status.HTTP_201_CREATED)
async def create_log(
    project_id: UUID,
    data: LogCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await log_service.create_log(db, project_id, data)


@router.get("/projects/{project_id}/logs", response_model=list[LogResponse])
async def list_logs(
    project_id: UUID,
    skill: str | None = None,
    task_id: UUID | None = None,
    limit: int | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await log_service.list_logs(db, project_id, skill=skill, task_id=task_id, limit=limit)
