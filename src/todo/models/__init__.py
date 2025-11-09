import pydantic

from .task import Task
from .project import Project

from .project_orm import ProjectORM
from .task_orm import TaskORM

pydantic.dataclasses.rebuild_dataclass(Project)
pydantic.dataclasses.rebuild_dataclass(Task)

__all__ = ["Task", "Project", "ProjectORM", "TaskORM"]
