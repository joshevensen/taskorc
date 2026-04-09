from uuid import UUID

from pydantic import BaseModel

from .base import BaseResponse


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    repo_url: str | None = None
    tech_stack: list[str] = []
    branch_prefix: str | None = None
    base_branch: str = "main"
    test_command: str | None = None
    lint_command: str | None = None
    format_command: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    repo_url: str | None = None
    tech_stack: list[str] | None = None
    branch_prefix: str | None = None
    base_branch: str | None = None
    test_command: str | None = None
    lint_command: str | None = None
    format_command: str | None = None


class ProjectResponse(BaseResponse):
    user_id: UUID
    name: str
    description: str | None
    repo_url: str | None
    tech_stack: list[str]
    branch_prefix: str | None
    base_branch: str | None
    test_command: str | None
    lint_command: str | None
    format_command: str | None
