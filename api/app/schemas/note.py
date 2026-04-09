import enum
from uuid import UUID

from pydantic import BaseModel

from .base import BaseResponse


class NoteCategory(str, enum.Enum):
    product = "product"
    strategy = "strategy"
    users = "users"
    market = "market"
    decisions = "decisions"
    constraints = "constraints"
    goals = "goals"
    general = "general"


class NoteCreate(BaseModel):
    title: str
    body: str
    category: NoteCategory


class NoteUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    category: NoteCategory | None = None


class NoteResponse(BaseResponse):
    project_id: UUID
    title: str
    body: str
    category: NoteCategory
