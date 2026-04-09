import enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel

from .base import BaseResponse


class LogOutcome(str, enum.Enum):
    success = "success"
    failure = "failure"
    skipped = "skipped"


class LogCreate(BaseModel):
    skill: str
    task_id: UUID | None = None
    duration: int | None = None
    outcome: LogOutcome
    summary: str | None = None
    metadata: dict[str, Any] | None = None


class LogResponse(BaseResponse):
    project_id: UUID
    task_id: UUID | None
    skill: str
    duration: int | None
    outcome: LogOutcome
    summary: str | None
    metadata: dict[str, Any] | None
