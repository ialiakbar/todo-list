from __future__ import annotations

import datetime
import uuid
from typing import Optional

from ..config.settings import settings
from ..models.project_orm import ProjectORM
from ..models.task_orm import TaskORM, TaskStatus
from ..repositories.interfaces import IProjectRepository, ITaskRepository
from ..exceptions.service import ValidationError, BusinessRuleError
from ..exceptions.repository import NotFoundError


class ToDoListManager:
    def __init__(
        self,
        project_repository: IProjectRepository,
        task_repository: ITaskRepository,
    ) -> None:
        """Initialize service with repositories via dependency injection."""
        self.project_repo = project_repository
        self.task_repo = task_repository

    def create_project(self, name: str, description: str = "") -> ProjectORM:
        """Create a new project with business rule validation."""
        # Business rule: check max number of projects
        project_count = self.project_repo.count()
        if project_count >= settings.MAX_NUMBER_OF_PROJECTS:
            raise BusinessRuleError(
                f"Cannot create more than {settings.MAX_NUMBER_OF_PROJECTS} projects"
            )

        # Create project (repository handles duplicate name check)
        try:
            project = self.project_repo.create(name, description)
            return project
        except NotFoundError:
            raise
        except Exception as e:
            # Convert repository exceptions to service exceptions
            if "already exists" in str(e).lower():
                raise BusinessRuleError(str(e)) from e
            raise

    def edit_project(
        self, project_id: str | uuid.UUID, name: str, description: str | None = None
    ) -> ProjectORM:
        """Edit an existing project."""
        project_uuid = uuid.UUID(project_id) if isinstance(project_id, str) else project_id
        project = self.project_repo.get_by_id(project_uuid)
        if project is None:
            raise NotFoundError("Project not found")

        project.update_details(name, description)
        try:
            return self.project_repo.update(project)
        except Exception as e:
            if "already exists" in str(e).lower():
                raise BusinessRuleError(str(e)) from e
            raise

    def delete_project(self, project_id: str | uuid.UUID) -> bool:
        """Delete a project (cascade delete handled by database)."""
        project_uuid = uuid.UUID(project_id) if isinstance(project_id, str) else project_id
        return self.project_repo.delete(project_uuid)

    def add_task_to_project(
        self,
        project_id: str | uuid.UUID,
        title: str,
        description: str = "",
        deadline: Optional[datetime.datetime] = None,
    ) -> TaskORM:
        """Add a task to a project with business rule validation."""
        project_uuid = uuid.UUID(project_id) if isinstance(project_id, str) else project_id
        
        # Check project exists
        project = self.project_repo.get_by_id(project_uuid)
        if project is None:
            raise NotFoundError("Project not found")

        # Business rule: check max number of tasks per project
        task_count = self.task_repo.count_by_project(project_uuid)
        if task_count >= settings.MAX_NUMBER_OF_TASKS:
            raise BusinessRuleError(
                f"Cannot add more than {settings.MAX_NUMBER_OF_TASKS} tasks to a project"
            )

        # Create task
        return self.task_repo.create(project_uuid, title, description, deadline)

    def change_task_status(
        self, task_id: str | uuid.UUID, new_status: TaskStatus
    ) -> TaskORM:
        """Change task status."""
        task_uuid = uuid.UUID(task_id) if isinstance(task_id, str) else task_id
        task = self.task_repo.get_by_id(task_uuid)
        if task is None:
            raise NotFoundError("Task not found")

        task.update_status(new_status)
        return self.task_repo.update(task)
    
    def edit_task(
        self,
        task_id: str | uuid.UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        deadline: Optional[datetime.datetime] = None,
        status: Optional[TaskStatus] = None,
    ) -> TaskORM:
        """Edit an existing task."""
        task_uuid = uuid.UUID(task_id) if isinstance(task_id, str) else task_id
        task = self.task_repo.get_by_id(task_uuid)
        if task is None:
            raise NotFoundError("Task not found")

        task.update_details(title, description, deadline)
        if status is not None:
            task.update_status(status)

        return self.task_repo.update(task)
    
    def delete_task(self, task_id: str | uuid.UUID) -> bool:
        """Delete a task."""
        task_uuid = uuid.UUID(task_id) if isinstance(task_id, str) else task_id
        return self.task_repo.delete(task_uuid)

    def list_all_projects(self) -> list[ProjectORM]:
        """List all projects."""
        return self.project_repo.get_all()

    def list_project_tasks(self, project_id: str | uuid.UUID) -> list[TaskORM]:
        """List all tasks for a project."""
        project_uuid = uuid.UUID(project_id) if isinstance(project_id, str) else project_id
        project = self.project_repo.get_by_id(project_uuid)
        if project is None:
            raise NotFoundError("Project not found")

        return self.task_repo.get_by_project_id(project_uuid)

    def get_project(self, project_id: str | uuid.UUID) -> Optional[ProjectORM]:
        """Get a project by ID (accepts string or UUID)."""
        project_uuid = uuid.UUID(project_id) if isinstance(project_id, str) else project_id
        return self.project_repo.get_by_id(project_uuid)

    def get_task(
        self, project_id: str | uuid.UUID, task_id: str | uuid.UUID
    ) -> Optional[TaskORM]:
        """Get a task by ID (optionally verify it belongs to project)."""
        task_uuid = uuid.UUID(task_id) if isinstance(task_id, str) else task_id
        task = self.task_repo.get_by_id(task_uuid)
        
        # Optionally verify task belongs to project
        if task and project_id:
            project_uuid = uuid.UUID(project_id) if isinstance(project_id, str) else project_id
            if task.project_id != project_uuid:
                return None

        return task
