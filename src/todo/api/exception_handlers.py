"""Exception handlers for consistent error responses."""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from ..exceptions.repository import NotFoundError, DuplicateError
from ..exceptions.service import ValidationError as ServiceValidationError, BusinessRuleError
from .controller_schemas.models import ErrorResponse, ErrorDetail


async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    """Handle NotFoundError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=ErrorResponse(
            success=False,
            error=ErrorDetail(
                code="resource_not_found",
                message=str(exc) or "Resource not found",
            ),
        ).model_dump(),
    )


async def duplicate_error_handler(request: Request, exc: DuplicateError) -> JSONResponse:
    """Handle DuplicateError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=ErrorResponse(
            success=False,
            error=ErrorDetail(
                code="duplicate_resource",
                message=str(exc) or "Resource already exists",
            ),
        ).model_dump(),
    )


async def validation_error_handler(request: Request, exc: ServiceValidationError) -> JSONResponse:
    """Handle service-level ValidationError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponse(
            success=False,
            error=ErrorDetail(
                code="validation_error",
                message=str(exc) or "Validation failed",
            ),
        ).model_dump(),
    )


async def business_rule_error_handler(request: Request, exc: BusinessRuleError) -> JSONResponse:
    """Handle BusinessRuleError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponse(
            success=False,
            error=ErrorDetail(
                code="business_rule_violation",
                message=str(exc) or "Business rule violation",
            ),
        ).model_dump(),
    )


async def request_validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle FastAPI request validation errors."""
    errors = exc.errors()
    error_messages = [f"{err['loc']}: {err['msg']}" for err in errors]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            success=False,
            error=ErrorDetail(
                code="request_validation_error",
                message="Request validation failed",
                details={"errors": error_messages},
            ),
        ).model_dump(),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            success=False,
            error=ErrorDetail(
                code="internal_server_error",
                message="An unexpected error occurred",
            ),
        ).model_dump(),
    )

