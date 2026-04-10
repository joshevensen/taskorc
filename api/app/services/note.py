from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.note import Note
from app.schemas.note import NoteCategory, NoteCreate, NoteUpdate
from app.services.ownership import assert_project_owner


async def create_note(db: AsyncSession, project_id: UUID, user_id: UUID, data: NoteCreate) -> Note:
    await assert_project_owner(db, project_id, user_id)
    note = Note(project_id=project_id, **data.model_dump())
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def list_notes(
    db: AsyncSession,
    project_id: UUID,
    user_id: UUID,
    category: NoteCategory | None = None,
    limit: int | None = None,
) -> list[Note]:
    await assert_project_owner(db, project_id, user_id)
    query = select(Note).where(Note.project_id == project_id)
    if category is not None:
        query = query.where(Note.category == category.value)
    if limit is not None:
        query = query.limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_note(db: AsyncSession, note_id: UUID, user_id: UUID) -> Note:
    result = await db.execute(select(Note).where(Note.id == note_id))
    note = result.scalar_one_or_none()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    await assert_project_owner(db, note.project_id, user_id)
    return note


async def update_note(db: AsyncSession, note_id: UUID, user_id: UUID, data: NoteUpdate) -> Note:
    note = await get_note(db, note_id, user_id)
    for field, value in data.model_dump(exclude_none=True).items():
        if hasattr(value, "value"):
            value = value.value
        setattr(note, field, value)
    await db.commit()
    await db.refresh(note)
    return note


async def delete_note(db: AsyncSession, note_id: UUID, user_id: UUID) -> None:
    note = await get_note(db, note_id, user_id)
    await db.delete(note)
    await db.commit()
