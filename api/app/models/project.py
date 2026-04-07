from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .artifact import Artifact
    from .log import Log
    from .note import Note
    from .task import Task
    from .user import User


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    repo_url: Mapped[str | None] = mapped_column(String, nullable=True)
    tech_stack: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True, default=[])
    branch_prefix: Mapped[str | None] = mapped_column(String, nullable=True)
    base_branch: Mapped[str | None] = mapped_column(String, nullable=True, default="main")
    test_command: Mapped[str | None] = mapped_column(String, nullable=True)
    lint_command: Mapped[str | None] = mapped_column(String, nullable=True)
    format_command: Mapped[str | None] = mapped_column(String, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="projects")
    tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="project", cascade="all, delete-orphan"
    )
    notes: Mapped[list["Note"]] = relationship(
        "Note", back_populates="project", cascade="all, delete-orphan"
    )
    logs: Mapped[list["Log"]] = relationship(
        "Log", back_populates="project", cascade="all, delete-orphan"
    )
    artifacts: Mapped[list["Artifact"]] = relationship(
        "Artifact",
        primaryjoin="and_(Project.id == foreign(Artifact.parent_id), Artifact.parent_type == 'project')",
        viewonly=True,
    )
