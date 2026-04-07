from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .user import User

artifact_type = ENUM(
    "figma", "video", "document", "error_log", "screenshot", "other",
    name="artifact_type",
)
artifact_parent_type = ENUM(
    "project", "task",
    name="artifact_parent_type",
)


class Artifact(Base, TimestampMixin):
    __tablename__ = "artifacts"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    type: Mapped[str] = mapped_column(artifact_type, nullable=False)
    parent_type: Mapped[str] = mapped_column(artifact_parent_type, nullable=False)
    # No FK constraint — polymorphic reference resolved at the service layer
    parent_id: Mapped[UUID] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship("User")
