"""Service layer exceptions."""

from .base import ToDoException


class ServiceException(ToDoException):
    """Base exception for service layer errors."""
    pass


class ValidationError(ServiceException):
    """Raised when validation fails."""
    pass


class BusinessRuleError(ServiceException):
    """Raised when a business rule is violated."""
    pass

