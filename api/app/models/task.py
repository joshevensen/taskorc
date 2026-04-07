from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .artifact import Artifact
    from .log import Log
    from .project import Project

task_status = ENUM(
    "draft", "planned", "in_progress", "complete", "failed", "on_hold", "cancelled",
    name="task_status",
)
execution_mode = ENUM(
    "guided", "autonomous",
    name="execution_mode",
)


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    project_id: Mapped[UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    problem: Mapped[str | None] = mapped_column(Text, nullable=True)
    acceptance_criteria: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    priority: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(task_status, nullable=False, default="draft")
    subtasks: Mapped[list[Any]] = mapped_column(JSONB, nullable=False, default=[])
    branch: Mapped[str | None] = mapped_column(String, nullable=True)
    pr_url: Mapped[str | None] = mapped_column(String, nullable=True)
    execution_mode: Mapped[str | None] = mapped_column(execution_mode, nullable=True)

    project: Mapped["Project"] = relationship("Project", back_populates="tasks")
    logs: Mapped[list["Log"]] = relationship("Log", back_populates="task")
    artifacts: Mapped[list["Artifact"]] = relationship(
        "Artifact",
        primaryjoin="and_(Task.id == foreign(Artifact.parent_id), Artifact.parent_type == 'task')",
        viewonly=True,
    )
