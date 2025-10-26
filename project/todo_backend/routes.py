from fastapi import APIRouter

from todo_backend.handlers.todos import router as todos_router


router = APIRouter()
router.include_router(todos_router)
