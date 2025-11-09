"""Repository interfaces (contracts) for data access layer."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional
import datetime
import uuid

from ..models.project_orm import ProjectORM
from ..models.task_orm import TaskORM, TaskStatus


class IProjectRepository(ABC):
    """Interface for Project repository operations."""

    @abstractmethod
    def create(self, name: str, description: str = "") -> ProjectORM:
        """Create a new project."""
        pass

    @abstractmethod
    def get_by_id(self, project_id: uuid.UUID) -> Optional[ProjectORM]:
        """Get a project by ID."""
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[ProjectORM]:
        """Get a project by name (case-insensitive)."""
        pass

    @abstractmethod
    def get_all(self) -> list[ProjectORM]:
        """Get all projects."""
        pass

    @abstractmethod
    def update(self, project: ProjectORM) -> ProjectORM:
        """Update an existing project."""
        pass

    @abstractmethod
    def delete(self, project_id: uuid.UUID) -> bool:
        """Delete a project by ID."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Count total number of projects."""
        pass


class ITaskRepository(ABC):
    """Interface for Task repository operations."""

    @abstractmethod
    def create(
        self,
        project_id: uuid.UUID,
        title: str,
        description: str = "",
        deadline: Optional[datetime.datetime] = None,
    ) -> TaskORM:
        """Create a new task."""
        pass

    @abstractmethod
    def get_by_id(self, task_id: uuid.UUID) -> Optional[TaskORM]:
        """Get a task by ID."""
        pass

    @abstractmethod
    def get_by_project_id(self, project_id: uuid.UUID) -> list[TaskORM]:
        """Get all tasks for a project."""
        pass

    @abstractmethod
    def update(self, task: TaskORM) -> TaskORM:
        """Update an existing task."""
        pass

    @abstractmethod
    def delete(self, task_id: uuid.UUID) -> bool:
        """Delete a task by ID."""
        pass

    @abstractmethod
    def count_by_project(self, project_id: uuid.UUID) -> int:
        """Count tasks for a project."""
        pass

    @abstractmethod
    def get_overdue_tasks(self) -> list[TaskORM]:
        """Get all overdue tasks that are not done."""
        pass

