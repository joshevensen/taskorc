import enum
from uuid import UUID

from pydantic import BaseModel

from .base import BaseResponse


class ArtifactType(str, enum.Enum):
    figma = "figma"
    video = "video"
    document = "document"
    error_log = "error_log"
    screenshot = "screenshot"
    other = "other"


class ArtifactParentType(str, enum.Enum):
    project = "project"
    task = "task"


class ArtifactCreate(BaseModel):
    title: str
    url: str
    body: str | None = None
    type: ArtifactType
    parent_type: ArtifactParentType
    parent_id: UUID


class ArtifactUpdate(BaseModel):
    title: str | None = None
    body: str | None = None


class ArtifactResponse(BaseResponse):
    user_id: UUID
    title: str
    url: str
    body: str | None
    type: ArtifactType
    parent_type: ArtifactParentType
    parent_id: UUID
