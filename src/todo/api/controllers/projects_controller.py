"""Project endpoints controller."""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..controller_schemas.models import Project, BaseResponse
from ...db.session import get_session
from ...factory import create_todo_manager_with_session
from ...services.todo_manager import ToDoListManager

router = APIRouter()


def get_todo_manager(db: Session = Depends(get_session)) -> ToDoListManager:
    """FastAPI dependency for ToDoListManager."""
    return create_todo_manager_with_session(db)


@router.get(
    "/projects",
    response_model=BaseResponse[List[Project]],
    status_code=status.HTTP_200_OK,
    summary="List all projects",
    description="Retrieve all projects with their task counts",
)
def list_projects(
    manager: ToDoListManager = Depends(get_todo_manager),
) -> BaseResponse[List[Project]]:
    """List all projects."""
    projects = manager.list_all_projects()
    
    # Convert ORM models to Pydantic models and add task counts
    project_data = []
    for project in projects:
        task_count = len(manager.list_project_tasks(project.id))
        project_dict = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at,
            "task_count": task_count,
        }
        project_data.append(Project(**project_dict))
    
    return BaseResponse(success=True, data=project_data)


@router.post(
    "/projects",
    response_model=BaseResponse[Project],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
    description="Create a new project with name and optional description",
)
def create_project(
    project: Project,
    manager: ToDoListManager = Depends(get_todo_manager),
    db: Session = Depends(get_session),
) -> BaseResponse[Project]:
    """Create a new project."""
    try:
        created_project = manager.create_project(project.name, project.description)
        db.commit()
        
        project_data = Project(
            id=created_project.id,
            name=created_project.name,
            description=created_project.description,
            created_at=created_project.created_at,
            task_count=0,
        )
        
        return BaseResponse(success=True, data=project_data)
    except Exception:
        db.rollback()
        raise


@router.get(
    "/projects/{project_id}",
    response_model=BaseResponse[Project],
    status_code=status.HTTP_200_OK,
    summary="Get a project by ID",
    description="Retrieve a single project by its unique identifier",
)
def get_project(
    project_id: str,
    manager: ToDoListManager = Depends(get_todo_manager),
) -> BaseResponse[Project]:
    """Get a project by ID."""
    project = manager.get_project(project_id)
    if project is None:
        from ...exceptions.repository import NotFoundError
        raise NotFoundError("Project not found")
    
    task_count = len(manager.list_project_tasks(project.id))
    project_data = Project(
        id=project.id,
        name=project.name,
        description=project.description,
        created_at=project.created_at,
        task_count=task_count,
    )
    
    return BaseResponse(success=True, data=project_data)


@router.put(
    "/projects/{project_id}",
    response_model=BaseResponse[Project],
    status_code=status.HTTP_200_OK,
    summary="Update a project",
    description="Update an existing project's name and description",
)
def update_project(
    project_id: str,
    project: Project,
    manager: ToDoListManager = Depends(get_todo_manager),
    db: Session = Depends(get_session),
) -> BaseResponse[Project]:
    """Update a project."""
    try:
        description = project.description if project.description else None
        updated_project = manager.edit_project(project_id, project.name, description)
        db.commit()
        
        task_count = len(manager.list_project_tasks(updated_project.id))
        project_data = Project(
            id=updated_project.id,
            name=updated_project.name,
            description=updated_project.description,
            created_at=updated_project.created_at,
            task_count=task_count,
        )
        
        return BaseResponse(success=True, data=project_data)
    except Exception:
        db.rollback()
        raise


@router.delete(
    "/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
    description="Delete a project and all its associated tasks (cascade delete)",
)
def delete_project(
    project_id: str,
    manager: ToDoListManager = Depends(get_todo_manager),
    db: Session = Depends(get_session),
) -> None:
    """Delete a project."""
    try:
        deleted = manager.delete_project(project_id)
        if not deleted:
            from ...exceptions.repository import NotFoundError
            raise NotFoundError("Project not found")
        db.commit()
    except Exception:
        db.rollback()
        raise

