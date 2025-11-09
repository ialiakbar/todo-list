"""SQLAlchemy implementation of Task repository."""

from __future__ import annotations

from typing import Optional
import datetime
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from ..models.task_orm import TaskORM, TaskStatus
from ..exceptions.repository import NotFoundError
from .interfaces import ITaskRepository


class TaskRepository(ITaskRepository):
    """SQLAlchemy-based implementation of Task repository."""

    def __init__(self, session: Session) -> None:
        """Initialize repository with a database session."""
        self.session = session

    def create(
        self,
        project_id: uuid.UUID,
        title: str,
        description: str = "",
        deadline: Optional[datetime.datetime] = None,
    ) -> TaskORM:
        """Create a new task."""
        task = TaskORM(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
        )
        self.session.add(task)
        self.session.flush()
        self.session.commit()
        return task

    def get_by_id(self, task_id: uuid.UUID) -> Optional[TaskORM]:
        """Get a task by ID."""
        return self.session.get(TaskORM, task_id)

    def get_by_project_id(self, project_id: uuid.UUID) -> list[TaskORM]:
        """Get all tasks for a project."""
        return self.session.query(TaskORM).filter(
            TaskORM.project_id == project_id
        ).order_by(TaskORM.created_at).all()

    def update(self, task: TaskORM) -> TaskORM:
        """Update an existing task."""
        self.session.flush()
        self.session.commit()
        return task

    def delete(self, task_id: uuid.UUID) -> bool:
        """Delete a task by ID."""
        task = self.get_by_id(task_id)
        if task is None:
            return False
        self.session.delete(task)
        return True

    def count_by_project(self, project_id: uuid.UUID) -> int:
        """Count tasks for a project."""
        return self.session.query(func.count(TaskORM.id)).filter(
            TaskORM.project_id == project_id
        ).scalar() or 0

    def get_overdue_tasks(self) -> list[TaskORM]:
        """Get all overdue tasks that are not done."""
        now = datetime.datetime.now(datetime.timezone.utc)
        return self.session.query(TaskORM).filter(
            and_(
                TaskORM.deadline.isnot(None),
                TaskORM.deadline < now,
                TaskORM.status != TaskStatus.DONE
            )
        ).all()

