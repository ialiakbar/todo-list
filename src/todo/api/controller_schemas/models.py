"""Pydantic models for API requests and responses."""

from __future__ import annotations

import datetime
import uuid
from typing import Optional, Generic, TypeVar, Any
from pydantic import BaseModel, Field, field_validator

from ...models.task_orm import TaskStatus
from ...config.settings import settings

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    """Base response envelope with success flag and data."""
    success: bool = Field(description="Whether the request was successful")
    data: T = Field(description="Response data payload")


class ErrorDetail(BaseModel):
    """Error detail structure."""
    code: str = Field(description="Error code identifier")
    message: str = Field(description="Human-readable error message")
    details: Optional[dict[str, Any]] = Field(default=None, description="Additional error details")


class ErrorResponse(BaseModel):
    """Error response envelope."""
    success: bool = Field(default=False, description="Always false for error responses")
    error: ErrorDetail = Field(description="Error information")


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(description="Health status")
    message: str = Field(description="Health check message")


class Project(BaseModel):
    """Project model for requests and responses. Use for both create and update operations."""
    id: Optional[uuid.UUID] = Field(default=None, description="Project unique identifier (auto-generated, omit on create)")
    name: str = Field(description="Project name", min_length=1, max_length=settings.MAX_PROJECT_NAME_LENGTH)
    description: str = Field(default="", description="Project description", max_length=settings.MAX_PROJECT_DESCRIPTION_LENGTH)
    created_at: Optional[datetime.datetime] = Field(default=None, description="Project creation timestamp (read-only)")
    task_count: Optional[int] = Field(default=None, description="Number of tasks in project (read-only)")

    model_config = {"from_attributes": True}


class Task(BaseModel):
    """Task model for requests and responses. Use for both create and update operations."""
    id: Optional[uuid.UUID] = Field(default=None, description="Task unique identifier (auto-generated, omit on create)")
    project_id: Optional[uuid.UUID] = Field(default=None, description="Parent project identifier (required on create, omit on update)")
    title: Optional[str] = Field(default=None, description="Task title", min_length=1, max_length=settings.MAX_TASK_TITLE_LENGTH)
    description: Optional[str] = Field(default=None, description="Task description", max_length=settings.MAX_TASK_DESCRIPTION_LENGTH)
    status: Optional[TaskStatus] = Field(default=None, description="Task status")
    deadline: Optional[datetime.datetime] = Field(default=None, description="Task deadline (ISO 8601 format)")
    created_at: Optional[datetime.datetime] = Field(default=None, description="Task creation timestamp (read-only)")
    closed_at: Optional[datetime.datetime] = Field(default=None, description="Task completion timestamp (read-only)")

    @field_validator("deadline")
    @classmethod
    def validate_deadline(cls, v: Optional[datetime.datetime]) -> Optional[datetime.datetime]:
        """Validate deadline is not in the past."""
        if v is not None:
            now = datetime.datetime.now(datetime.timezone.utc)
            if v < now:
                raise ValueError("Deadline cannot be in the past")
        return v

    model_config = {"from_attributes": True}

