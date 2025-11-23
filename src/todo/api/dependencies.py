"""FastAPI dependencies for database sessions and services."""

from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from ...db.session import SessionLocal
from ...factory import create_todo_manager_with_session
from ...services.todo_manager import ToDoListManager


def get_db() -> Generator[Session, None, None]:
    """Dependency that provides a database session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_todo_manager(
    db: Session = Depends(get_db),
) -> ToDoListManager:
    """Dependency that provides a ToDoListManager instance."""
    return create_todo_manager_with_session(db)

