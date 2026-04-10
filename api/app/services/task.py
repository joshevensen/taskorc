from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified

from app.models.task import Task
from app.schemas.task import SubtaskItem, TaskCreate, TaskStatus, TaskUpdate
from app.services.ownership import assert_project_owner


async def create_task(db: AsyncSession, project_id: UUID, user_id: UUID, data: TaskCreate) -> Task:
    await assert_project_owner(db, project_id, user_id)
    task = Task(project_id=project_id, **data.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def list_tasks(
    db: AsyncSession,
    project_id: UUID,
    user_id: UUID,
    status: TaskStatus | None = None,
    limit: int | None = None,
) -> list[Task]:
    await assert_project_owner(db, project_id, user_id)
    query = select(Task).where(Task.project_id == project_id)
    if status is not None:
        query = query.where(Task.status == status.value)
    if limit is not None:
        query = query.limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_task(db: AsyncSession, task_id: UUID, user_id: UUID) -> Task:
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await assert_project_owner(db, task.project_id, user_id)
    return task


async def update_task(db: AsyncSession, task_id: UUID, user_id: UUID, data: TaskUpdate) -> Task:
    task = await get_task(db, task_id, user_id)
    for field, value in data.model_dump(exclude_none=True).items():
        # Store enum values as their string value for the DB column
        if hasattr(value, "value"):
            value = value.value
        setattr(task, field, value)
    await db.commit()
    await db.refresh(task)
    return task


async def set_subtasks(db: AsyncSession, task_id: UUID, user_id: UUID, subtasks: list[SubtaskItem]) -> Task:
    task = await get_task(db, task_id, user_id)
    task.subtasks = [s.model_dump() for s in subtasks]
    flag_modified(task, "subtasks")
    await db.commit()
    await db.refresh(task)
    return task


async def complete_subtask(db: AsyncSession, task_id: UUID, subtask_id: str, user_id: UUID) -> Task:
    task = await get_task(db, task_id, user_id)
    subtasks = task.subtasks or []
    matched = any(s.get("id") == subtask_id for s in subtasks)
    if not matched:
        raise HTTPException(status_code=404, detail="Subtask not found")
    # Build a new list with new dict objects so SQLAlchemy detects the JSONB change
    task.subtasks = [
        {**s, "completed": True} if s.get("id") == subtask_id else dict(s)
        for s in subtasks
    ]
    flag_modified(task, "subtasks")
    await db.commit()
    await db.refresh(task)
    return task


async def next_task(db: AsyncSession, project_id: UUID, user_id: UUID) -> Task | None:
    await assert_project_owner(db, project_id, user_id)
    result = await db.execute(
        select(Task)
        .where(Task.project_id == project_id)
        .where(Task.status == TaskStatus.planned.value)
        .where(Task.priority.is_not(None))
        .order_by(Task.priority.asc())
        .limit(1)
    )
    return result.scalar_one_or_none()
