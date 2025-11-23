"""Health check endpoint controller."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    message: str


@router.get("/health", response_model=HealthResponse, summary="Health check", description="Check API health status")
def health_check() -> HealthResponse:
    """Health check endpoint to verify API is running."""
    return HealthResponse(status="healthy", message="ToDoList API is running")

