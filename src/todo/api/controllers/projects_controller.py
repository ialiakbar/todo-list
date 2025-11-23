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

