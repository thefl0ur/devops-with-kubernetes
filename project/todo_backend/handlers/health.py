"""Health check handlers for the backend application."""

from fastapi import APIRouter

from todo_backend.models import TodoModel


router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint for liveness probe."""
    return {"status": "healthy"}


@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint that verifies database connectivity."""
    try:
        await TodoModel.all().count()
        return {"status": "ready"}
    except Exception as e:
        return {"status": "not ready", "error": str(e)}
