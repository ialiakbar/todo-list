"""SQLAlchemy ORM model for Project."""

from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, func, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base
from ..config.settings import settings

if TYPE_CHECKING:
    from .task_orm import TaskORM


class ProjectORM(Base):
    """SQLAlchemy ORM model for Project entity."""

    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(settings.MAX_PROJECT_NAME_LENGTH),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(settings.MAX_PROJECT_DESCRIPTION_LENGTH),
        nullable=False,
        default="",
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # Relationship to tasks (one-to-many)
    tasks: Mapped[list["TaskORM"]] = relationship(
        "TaskORM",
        back_populates="project",
        cascade="all, delete-orphan",
    )

    def update_details(self, name: str | None = None, description: str | None = None) -> None:
        """Update project name and/or description."""
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description

