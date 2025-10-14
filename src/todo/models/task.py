from __future__ import annotations

import uuid
import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING

from pydantic import Field
from pydantic.dataclasses import dataclass as pydantic_dataclass

from ..config.settings import settings

if TYPE_CHECKING:
    from .project import Project


class TaskStatus(str, Enum):
    TODO = "TODO"
    DOING = "DOING"
    DONE = "DONE"


@pydantic_dataclass
class Task:
    project: Project
    id: str = Field(
        default_factory=uuid.uuid4
    )
    title: str = Field(
        ...,
        min_length=1,
        max_length=settings.MAX_TASK_TITLE_LENGTH,
    )
    description: str = Field(
        default_factory=str,
        max_length=settings.MAX_TASK_DESCRIPTION_LENGTH,
    )
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
    )
    status: TaskStatus = TaskStatus.TODO
    deadline: Optional[datetime.datetime] = None

    def update_status(self, new_status: TaskStatus) -> None:
        self.status = new_status

    def update_details(
            self,
            title: Optional[str] = None,
            description: Optional[str] = None,
            deadline: Optional[datetime.datetime] = None
    ) -> None:
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if deadline is not None:
            self.deadline = deadline
