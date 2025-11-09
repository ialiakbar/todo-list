"""Repository layer exceptions."""

from .base import ToDoException


class RepositoryException(ToDoException):
    """Base exception for repository layer errors."""
    pass


class NotFoundError(RepositoryException):
    """Raised when a requested entity is not found."""
    pass


class DuplicateError(RepositoryException):
    """Raised when attempting to create a duplicate entity."""
    pass

