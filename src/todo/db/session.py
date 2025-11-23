"""Database session factory and management."""

from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from ..config.settings import settings
from .base import Base


engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_session() -> Generator[Session, None, None]:
    """Provides a database session generator."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


get_session_ctx = contextmanager(get_session)


def init_db() -> None:
    """Initialize database tables (for development/testing only)."""
    Base.metadata.create_all(bind=engine)
