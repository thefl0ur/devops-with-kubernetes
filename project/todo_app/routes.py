from fastapi import APIRouter

from todo_app.handlers.health import router as health_router
from todo_app.handlers.index import router as index_router


router = APIRouter()
router.include_router(index_router)
router.include_router(health_router)
