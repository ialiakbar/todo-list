"""Task endpoints controller."""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..controller_schemas.models import Task, BaseResponse
from ...db.session import get_session
from ...factory import create_todo_manager_with_session
from ...services.todo_manager import ToDoListManager

router = APIRouter()


def get_todo_manager(db: Session = Depends(get_session)) -> ToDoListManager:
    """FastAPI dependency for ToDoListManager."""
    return create_todo_manager_with_session(db)


@router.get(
    "/projects/{project_id}/tasks",
    response_model=BaseResponse[List[Task]],
    status_code=status.HTTP_200_OK,
    summary="List tasks in a project",
    description="Retrieve all tasks belonging to a specific project",
)
def list_project_tasks(
    project_id: str,
    manager: ToDoListManager = Depends(get_todo_manager),
) -> BaseResponse[List[Task]]:
    """List all tasks for a project."""
    tasks = manager.list_project_tasks(project_id)
    
    # Convert ORM models to Pydantic models
    task_data = []
    for task in tasks:
        task_dict = {
            "id": task.id,
            "project_id": task.project_id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "deadline": task.deadline,
            "created_at": task.created_at,
            "closed_at": task.closed_at,
        }
        task_data.append(Task(**task_dict))
    
    return BaseResponse(success=True, data=task_data)


@router.post(
    "/projects/{project_id}/tasks",
    response_model=BaseResponse[Task],
    status_code=status.HTTP_201_CREATED,
    summary="Create a task in a project",
    description="Create a new task within a specific project",
)
def create_task(
    project_id: str,
    task: Task,
    manager: ToDoListManager = Depends(get_todo_manager),
    db: Session = Depends(get_session),
) -> BaseResponse[Task]:
    """Create a new task in a project."""
    try:
        # Validate that title is provided (required for create)
        if not task.title:
            from ...exceptions.service import ValidationError
            raise ValidationError("Task title is required")
        
        created_task = manager.add_task_to_project(
            project_id,
            task.title,
            task.description or "",
            task.deadline,
        )
        db.commit()
        
        task_data = Task(
            id=created_task.id,
            project_id=created_task.project_id,
            title=created_task.title,
            description=created_task.description,
            status=created_task.status,
            deadline=created_task.deadline,
            created_at=created_task.created_at,
            closed_at=created_task.closed_at,
        )
        
        return BaseResponse(success=True, data=task_data)
    except Exception:
        db.rollback()
        raise

