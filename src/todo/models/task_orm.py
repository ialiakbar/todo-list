"""SQLAlchemy ORM model for Task."""

from __future__ import annotations

import datetime
import uuid
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, DateTime, func, UUID, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base
from ..config.settings import settings

if TYPE_CHECKING:
    from .project_orm import ProjectORM


class TaskStatus(str, Enum):
    """Task status enumeration."""
    TODO = "TODO"
    DOING = "DOING"
    DONE = "DONE"


class TaskORM(Base):
    """SQLAlchemy ORM model for Task entity."""

    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=uuid.uuid4,
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(settings.MAX_TASK_TITLE_LENGTH),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(settings.MAX_TASK_DESCRIPTION_LENGTH),
        nullable=False,
        default="",
    )
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus, native_enum=False),
        nullable=False,
        default=TaskStatus.TODO,
    )
    deadline: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    closed_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationship to project (many-to-one)
    project: Mapped["ProjectORM"] = relationship(
        "ProjectORM",
        back_populates="tasks",
    )

    def update_status(self, new_status: TaskStatus) -> None:
        """Update task status."""
        self.status = new_status
        if new_status == TaskStatus.DONE and self.closed_at is None:
            self.closed_at = datetime.datetime.now(datetime.timezone.utc)
        elif new_status != TaskStatus.DONE:
            self.closed_at = None

    def update_details(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        deadline: Optional[datetime.datetime] = None,
    ) -> None:
        """Update task details."""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if deadline is not None:
            self.deadline = deadline

