"""Health check handlers for the frontend application."""

import httpx

from fastapi import APIRouter

from todo_app.config import settings


router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint for liveness probe."""
    return {"status": "healthy"}


@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint that verifies backend connectivity."""
    try:
        # Extract the base URL from the backend address to form the health check URL
        # BACKEND_ADDRESS is typically "http://todo-app-backend-service.project:80/todos"
        # We need to replace "/todos" with "/health" to form the health check URL
        base_url = settings.backend_address.rsplit("/", 1)[0]  # Remove the last segment ("/todos")
        health_url = f"{base_url}/health"

        # Check if backend is accessible
        async with httpx.AsyncClient() as client:
            response = await client.get(health_url, timeout=5.0)
            if response.status_code == 200:
                return {"status": "ready"}
            else:
                return {
                    "status": "not ready",
                    "error": f"Backend returned status {response.status_code}",
                }
    except Exception as e:
        return {"status": "not ready", "error": str(e)}
