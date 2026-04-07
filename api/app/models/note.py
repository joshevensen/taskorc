from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .project import Project

note_category = ENUM(
    "product", "strategy", "users", "market", "decisions", "constraints", "goals", "general",
    name="note_category",
)


class Note(Base, TimestampMixin):
    __tablename__ = "notes"

    project_id: Mapped[UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(note_category, nullable=False)

    project: Mapped["Project"] = relationship("Project", back_populates="notes")
