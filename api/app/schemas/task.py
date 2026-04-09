import enum
from uuid import UUID

from pydantic import BaseModel

from .base import BaseResponse


class TaskStatus(str, enum.Enum):
    draft = "draft"
    planned = "planned"
    in_progress = "in_progress"
    complete = "complete"
    failed = "failed"
    on_hold = "on_hold"
    cancelled = "cancelled"


class ExecutionMode(str, enum.Enum):
    guided = "guided"
    autonomous = "autonomous"


class SubtaskItem(BaseModel):
    id: str
    description: str
    prompt: str
    completed: bool = False


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    problem: str | None = None
    acceptance_criteria: list[str] | None = None
    priority: int | None = None
    status: TaskStatus = TaskStatus.draft


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    problem: str | None = None
    acceptance_criteria: list[str] | None = None
    priority: int | None = None
    status: TaskStatus | None = None
    branch: str | None = None
    pr_url: str | None = None
    execution_mode: ExecutionMode | None = None


class TaskResponse(BaseResponse):
    project_id: UUID
    title: str
    description: str | None
    problem: str | None
    acceptance_criteria: list[str] | None
    priority: int | None
    status: TaskStatus
    subtasks: list[SubtaskItem]
    branch: str | None
    pr_url: str | None
    execution_mode: ExecutionMode | None
