from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db import get_db
from app.models.user import User
from app.schemas.note import NoteCategory, NoteCreate, NoteResponse, NoteUpdate
from app.services import note as note_service

router = APIRouter(tags=["notes"])


@router.post("/projects/{project_id}/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    project_id: UUID,
    data: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await note_service.create_note(db, project_id, current_user.id, data)


@router.get("/projects/{project_id}/notes", response_model=list[NoteResponse])
async def list_notes(
    project_id: UUID,
    category: NoteCategory | None = None,
    limit: int | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await note_service.list_notes(db, project_id, current_user.id, category=category, limit=limit)


@router.get("/notes/{id}", response_model=NoteResponse)
async def get_note(
    id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await note_service.get_note(db, id, current_user.id)


@router.patch("/notes/{id}", response_model=NoteResponse)
async def update_note(
    id: UUID,
    data: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await note_service.update_note(db, id, current_user.id, data)


@router.delete("/notes/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await note_service.delete_note(db, id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
