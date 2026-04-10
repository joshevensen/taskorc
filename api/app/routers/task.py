from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db import get_db
from app.models.user import User
from app.schemas.task import SubtaskItem, TaskCreate, TaskResponse, TaskStatus, TaskUpdate
from app.services import task as task_service

router = APIRouter(tags=["tasks"])


@router.post("/projects/{project_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    project_id: UUID,
    data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await task_service.create_task(db, project_id, current_user.id, data)


@router.get("/projects/{project_id}/tasks/next", response_model=TaskResponse)
async def get_next_task(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Must be registered before /projects/{project_id}/tasks to avoid route conflict
    task = await task_service.next_task(db, project_id, current_user.id)
    if task is None:
        raise HTTPException(status_code=404, detail="No planned tasks with priority set")
    return task


@router.get("/projects/{project_id}/tasks", response_model=list[TaskResponse])
async def list_tasks(
    project_id: UUID,
    status: TaskStatus | None = None,
    limit: int | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await task_service.list_tasks(db, project_id, current_user.id, status=status, limit=limit)


@router.get("/tasks/{id}", response_model=TaskResponse)
async def get_task(
    id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await task_service.get_task(db, id, current_user.id)


@router.patch("/tasks/{id}", response_model=TaskResponse)
async def update_task(
    id: UUID,
    data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await task_service.update_task(db, id, current_user.id, data)


@router.put("/tasks/{id}/subtasks", response_model=TaskResponse)
async def set_subtasks(
    id: UUID,
    subtasks: list[SubtaskItem],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await task_service.set_subtasks(db, id, current_user.id, subtasks)


@router.post("/tasks/{id}/subtasks/{subtask_id}/complete", response_model=TaskResponse)
async def complete_subtask(
    id: UUID,
    subtask_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await task_service.complete_subtask(db, id, current_user.id, subtask_id)
