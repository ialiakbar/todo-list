"""API router configuration and endpoint registration."""

from fastapi import APIRouter

from .controllers import health_controller, projects_controller, tasks_controller

# Create main API router
api_router = APIRouter()

# Register route handlers
api_router.include_router(health_controller.router, tags=["health"])
api_router.include_router(projects_controller.router, tags=["projects"])
api_router.include_router(tasks_controller.router, tags=["tasks"])

