from __future__ import annotations

import datetime
from typing import Dict, List, Optional

from ..config.settings import settings
from ..models import Project, Task
from ..models.task import TaskStatus


class ToDoListManager:
    def __init__(self) -> None:
        self.projects: Dict[str, Project] = dict()
        self.tasks: Dict[str, Task] = dict()

    def create_project(self, name: str, description: str = "") -> Project:
        if len(self.projects) >= settings.MAX_NUMBER_OF_PROJECTS:
            raise ValueError(f"Cannot create more than {settings.MAX_NUMBER_OF_PROJECTS} projects")

        for project in self.projects.values():
            if project.name.lower() == name.lower():
                raise ValueError("A project with this name already exists")

        project = Project(
            name=name,
            description=description
        )

        self.projects[project.id] = project
        return project

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
            title=title,
            description=description,
            deadline=deadline
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

    def list_all_projects(self) -> List[Project]:
        return sorted(self.projects.values(), key=lambda p: p.created_at)

    def list_project_tasks(self, project_id: str) -> List[Task]:
        if project := self.get_project(project_id):
            return project.get_all_tasks()
        else:
            raise ValueError("Project not found")

    def get_project(self, project_id: str) -> Optional[Project]:
        return self.projects.get(project_id)

    def get_task(self, project_id: str, task_id: str) -> Optional[Task]:
        project = self.get_project(project_id)
        if project is None:
            return None
        return project.get_task(task_id)
