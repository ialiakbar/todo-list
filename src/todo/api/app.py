"""FastAPI application factory and configuration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import api_router
from .exception_handlers import (
    not_found_handler,
    duplicate_error_handler,
    validation_error_handler,
    business_rule_error_handler,
    request_validation_error_handler,
    generic_exception_handler,
)
from ..exceptions.repository import NotFoundError, DuplicateError
from ..exceptions.service import ValidationError as ServiceValidationError, BusinessRuleError
from fastapi.exceptions import RequestValidationError


def create_app() -> FastAPI:
    """Create and configure FastAPI application instance."""
    app = FastAPI(
        title="ToDoList API",
        description="RESTful Web API for ToDoList application with project and task management",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS middleware (configure as needed for production)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register exception handlers
    app.add_exception_handler(NotFoundError, not_found_handler)
    app.add_exception_handler(DuplicateError, duplicate_error_handler)
    app.add_exception_handler(ServiceValidationError, validation_error_handler)
    app.add_exception_handler(BusinessRuleError, business_rule_error_handler)
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    # Include API routers
    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()

