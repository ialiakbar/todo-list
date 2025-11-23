"""Dependency injection factory for creating services and repositories."""

from __future__ import annotations

from sqlalchemy.orm import Session

from .db.session import get_session_ctx
from .repositories import ProjectRepository, TaskRepository
from .repositories.interfaces import IProjectRepository, ITaskRepository
from .services.todo_manager import ToDoListManager


def create_project_repository(session: Session) -> IProjectRepository:
    """Create a Project repository instance."""
    return ProjectRepository(session)


def create_task_repository(session: Session) -> ITaskRepository:
    """Create a Task repository instance."""
    return TaskRepository(session)


def create_todo_manager(
    project_repository: IProjectRepository | None = None,
    task_repository: ITaskRepository | None = None,
    session: Session | None = None,
) -> ToDoListManager:
    """Create a ToDoListManager instance with dependencies.

    Args:
        project_repository: Optional project repository (created if not provided)
        task_repository: Optional task repository (created if not provided)
        session: Optional database session (required if repositories not provided)

    Returns:
        ToDoListManager instance with wired dependencies
    """
    if project_repository is None or task_repository is None:
        if session is None:
            raise ValueError("Session is required when repositories are not provided")
        project_repository = project_repository or create_project_repository(session)
        task_repository = task_repository or create_task_repository(session)

    return ToDoListManager(
        project_repository=project_repository,
        task_repository=task_repository,
    )


def create_todo_manager_with_session(session: Session) -> ToDoListManager:
    """Create a ToDoListManager instance using a provided session.

    Convenience function that creates repositories and manager in one call.

    Args:
        session: Database session

    Returns:
        ToDoListManager instance with wired dependencies
    """
    project_repo = create_project_repository(session)
    task_repo = create_task_repository(session)
    return create_todo_manager(project_repository=project_repo, task_repository=task_repo)

