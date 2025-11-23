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


@router.get(
    "/tasks/{task_id}",
    response_model=BaseResponse[Task],
    status_code=status.HTTP_200_OK,
    summary="Get a task by ID",
    description="Retrieve a single task by its unique identifier",
)
def get_task(
    task_id: str,
    manager: ToDoListManager = Depends(get_todo_manager),
) -> BaseResponse[Task]:
    """Get a task by ID."""
    task = manager.get_task(None, task_id)
    if task is None:
        from ...exceptions.repository import NotFoundError
        raise NotFoundError("Task not found")
    
    task_data = Task(
        id=task.id,
        project_id=task.project_id,
        title=task.title,
        description=task.description,
        status=task.status,
        deadline=task.deadline,
        created_at=task.created_at,
        closed_at=task.closed_at,
    )
    
    return BaseResponse(success=True, data=task_data)


@router.put(
    "/tasks/{task_id}",
    response_model=BaseResponse[Task],
    status_code=status.HTTP_200_OK,
    summary="Update a task",
    description="Update an existing task's details (partial update supported)",
)
def update_task(
    task_id: str,
    task: Task,
    manager: ToDoListManager = Depends(get_todo_manager),
    db: Session = Depends(get_session),
) -> BaseResponse[Task]:
    """Update a task."""
    try:
        from ...models.task_orm import TaskStatus
        
        # Get existing task to preserve fields not provided
        existing_task = manager.get_task(None, task_id)
        if existing_task is None:
            from ...exceptions.repository import NotFoundError
            raise NotFoundError("Task not found")
        
        # Use provided values or keep existing ones
        title = task.title if task.title is not None else existing_task.title
        description = task.description if task.description is not None else existing_task.description
        deadline = task.deadline if task.deadline is not None else existing_task.deadline
        status_value = task.status if task.status is not None else existing_task.status
        
        updated_task = manager.edit_task(
            task_id,
            title,
            description,
            deadline,
            status_value,
        )
        db.commit()
        
        task_data = Task(
            id=updated_task.id,
            project_id=updated_task.project_id,
            title=updated_task.title,
            description=updated_task.description,
            status=updated_task.status,
            deadline=updated_task.deadline,
            created_at=updated_task.created_at,
            closed_at=updated_task.closed_at,
        )
        
        return BaseResponse(success=True, data=task_data)
    except Exception:
        db.rollback()
        raise


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Delete a task by its unique identifier",
)
def delete_task(
    task_id: str,
    manager: ToDoListManager = Depends(get_todo_manager),
    db: Session = Depends(get_session),
) -> None:
    """Delete a task."""
    try:
        deleted = manager.delete_task(task_id)
        if not deleted:
            from ...exceptions.repository import NotFoundError
            raise NotFoundError("Task not found")
        db.commit()
    except Exception:
        db.rollback()
        raise


@router.patch(
    "/tasks/{task_id}/status",
    response_model=BaseResponse[Task],
    status_code=status.HTTP_200_OK,
    summary="Change task status",
    description="Update only the status of a task",
)
def change_task_status(
    task_id: str,
    task: Task,
    manager: ToDoListManager = Depends(get_todo_manager),
    db: Session = Depends(get_session),
) -> BaseResponse[Task]:
    """Change task status."""
    try:
        if task.status is None:
            from ...exceptions.service import ValidationError
            raise ValidationError("Status is required")
        
        updated_task = manager.change_task_status(task_id, task.status)
        db.commit()
        
        task_data = Task(
            id=updated_task.id,
            project_id=updated_task.project_id,
            title=updated_task.title,
            description=updated_task.description,
            status=updated_task.status,
            deadline=updated_task.deadline,
            created_at=updated_task.created_at,
            closed_at=updated_task.closed_at,
        )
        
        return BaseResponse(success=True, data=task_data)
    except Exception:
        db.rollback()
        raise

