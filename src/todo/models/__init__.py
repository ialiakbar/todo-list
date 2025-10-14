import pydantic

from .task import Task
from .project import Project

pydantic.dataclasses.rebuild_dataclass(Project)
pydantic.dataclasses.rebuild_dataclass(Task)

__all__ = ["Task", "Project"]
