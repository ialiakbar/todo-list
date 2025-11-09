"""SQLAlchemy implementation of Project repository."""

from __future__ import annotations

from typing import Optional
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.project_orm import ProjectORM
from ..exceptions.repository import NotFoundError, DuplicateError
from .interfaces import IProjectRepository


class ProjectRepository(IProjectRepository):
    """SQLAlchemy-based implementation of Project repository."""

    def __init__(self, session: Session) -> None:
        """Initialize repository with a database session."""
        self.session = session

    def create(self, name: str, description: str = "") -> ProjectORM:
        """Create a new project."""
        # Check for duplicate name (case-insensitive)
        existing = self.get_by_name(name)
        if existing is not None:
            raise DuplicateError(f"A project with name '{name}' already exists")

        project = ProjectORM(name=name, description=description)
        self.session.add(project)
        self.session.flush()
        self.session.commit()
        return project

    def get_by_id(self, project_id: uuid.UUID) -> Optional[ProjectORM]:
        """Get a project by ID."""
        return self.session.get(ProjectORM, project_id)

    def get_by_name(self, name: str) -> Optional[ProjectORM]:
        """Get a project by name (case-insensitive)."""
        return self.session.query(ProjectORM).filter(
            func.lower(ProjectORM.name) == func.lower(name)
        ).first()

    def get_all(self) -> list[ProjectORM]:
        """Get all projects."""
        return self.session.query(ProjectORM).order_by(ProjectORM.created_at).all()

    def update(self, project: ProjectORM) -> ProjectORM:
        """Update an existing project."""
        # Check for duplicate name if name changed
        if project.name:
            existing = self.session.query(ProjectORM).filter(
                func.lower(ProjectORM.name) == func.lower(project.name),
                ProjectORM.id != project.id
            ).first()
            if existing is not None:
                raise DuplicateError(f"A project with name '{project.name}' already exists")

        self.session.flush()
        self.session.commit()
        return project

    def delete(self, project_id: uuid.UUID) -> bool:
        """Delete a project by ID."""
        project = self.get_by_id(project_id)
        if project is None:
            return False
        self.session.delete(project)
        return True

    def count(self) -> int:
        """Count total number of projects."""
        return self.session.query(func.count(ProjectORM.id)).scalar() or 0

