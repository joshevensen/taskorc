from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.log import Log
from app.schemas.log import LogCreate


async def create_log(db: AsyncSession, project_id: UUID, data: LogCreate) -> Log:
    log_data = data.model_dump()
    # Map schema field `metadata` to model column `metadata_` (avoiding Python builtin clash)
    metadata = log_data.pop("metadata", None)
    log = Log(project_id=project_id, metadata_=metadata, **log_data)
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


async def list_logs(
    db: AsyncSession,
    project_id: UUID,
    skill: str | None = None,
    task_id: UUID | None = None,
    limit: int | None = None,
) -> list[Log]:
    query = select(Log).where(Log.project_id == project_id)
    if skill is not None:
        query = query.where(Log.skill == skill)
    if task_id is not None:
        query = query.where(Log.task_id == task_id)
    if limit is not None:
        query = query.limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())
