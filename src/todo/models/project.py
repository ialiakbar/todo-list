from __future__ import annotations

import uuid
import datetime
from typing import Dict, List

from pydantic.dataclasses import dataclass as pydantic_dataclass
from pydantic import Field

from .task import Task
from ..config.settings import settings


@pydantic_dataclass
class Project:
    id: str = Field(
        default_factory=uuid.uuid4
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=settings.MAX_PROJECT_NAME_LENGTH
    )
    description: str = Field(
        default_factory=str,
        max_length=settings.MAX_PROJECT_DESCRIPTION_LENGTH
    )
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now
    )
    tasks: Dict[str, Task] = Field(
        default_factory=dict
    )

    def add_task(self, task: Task) -> None:
        self.tasks[task.id] = task

    def remove_task(self, task_id: str) -> bool:
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def get_task(self, task_id: str) -> Task | None:
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        return sorted(self.tasks.values(), key=lambda t: t.created_at)

    def update_details(self, name: str = None, description: str = None) -> None:
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
