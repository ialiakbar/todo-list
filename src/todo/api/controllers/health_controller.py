"""Health check endpoint controller."""

from fastapi import APIRouter

from ..controller_schemas.models import HealthResponse, BaseResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=BaseResponse[HealthResponse],
    summary="Health check",
    description="Check API health status",
)
def health_check() -> BaseResponse[HealthResponse]:
    """Health check endpoint to verify API is running."""
    return BaseResponse(
        success=True,
        data=HealthResponse(status="healthy", message="ToDoList API is running"),
    )

