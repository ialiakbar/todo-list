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

    def edit_project(self, project_id: str, name: str, description: str = None) -> Project:
        if project_id not in self.projects:
            raise ValueError("Project not found")

        for pid, project in self.projects.items():
            if pid != project_id and project.name.lower() == name.lower():
                raise ValueError("A project with this name already exists")

        project = self.get_project(project_id)
        project.update_details(name, description)
        return project

    def delete_project(self, project_id: str) -> bool:
        if project_id not in self.projects:
            return False

        for _, task in self.projects[project_id].tasks.items():
            del self.tasks[task.id]

        del self.projects[project_id]

        return True

    def add_task_to_project(
        self,
        project_id: str,
        title: str,
        description: str = "",
        deadline: Optional[datetime.datetime] = None
    ) -> Task:
        if project_id not in self.projects:
            raise ValueError("Project not found")

        project = self.get_project(project_id)
        if len(project.tasks) >= settings.MAX_NUMBER_OF_TASKS:
            raise ValueError(f"Cannot add more than {settings.MAX_NUMBER_OF_TASKS} tasks to a project")

        task = Task(
            project=project,
            title=title,
            description=description,
            deadline=deadline,
        )
        project.add_task(task)
        self.tasks[task.id] = task
        return task

    def change_task_status(self, task_id: str, new_status: TaskStatus) -> Task:
        task = self.tasks.get(task_id)
        if task is None:
            raise ValueError("Task not found")

        task.update_status(new_status)
        return task
    
    def edit_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        deadline: Optional[datetime.datetime] = None,
        status: Optional[TaskStatus] = None,
    ) -> Task:
        task = self.tasks.get(task_id)
        if task is None:
            raise ValueError("Task not found")

        task.update_details(title, description, deadline)
        if status is not None:
            task.update_status(status)

        return task
    
    def delete_task(self, task_id: str) -> bool:
        task = self.tasks.get(task_id)
        if task is None:
            return False

        if project := self.get_project(task.project.id):
            project.remove_task(task_id)
        del self.tasks[task_id]
        del task
        return True

    def list_all_projects(self) -> list[ProjectORM]:
        """List all projects."""
        return self.project_repo.get_all()

    def list_project_tasks(self, project_id: str) -> List[Task]:
        if project := self.get_project(project_id):
            return project.get_all_tasks()
        else:
            raise ValueError("Project not found")

    def get_project(self, project_id: str | uuid.UUID) -> Optional[ProjectORM]:
        """Get a project by ID (accepts string or UUID)."""
        project_uuid = uuid.UUID(project_id) if isinstance(project_id, str) else project_id
        return self.project_repo.get_by_id(project_uuid)

    def get_task(self, project_id: str, task_id: str) -> Optional[Task]:
        project = self.get_project(project_id)
        if project is None:
            return None
        return project.get_task(task_id)
