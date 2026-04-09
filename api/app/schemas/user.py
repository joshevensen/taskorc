from typing import Any

from pydantic import BaseModel

from .base import BaseResponse


class UserResponse(BaseResponse):
    name: str
    email: str
    settings: dict[str, Any]
    founder_notes: str | None


class UserUpdateRequest(BaseModel):
    founder_notes: str | None = None
    settings: dict[str, Any] | None = None
