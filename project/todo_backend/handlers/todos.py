import logging

from typing import Annotated

from fastapi import APIRouter, Body, HTTPException

from todo_backend.handlers.schemas import TodoSchema
from todo_backend.models import TodoModel


router = APIRouter()

logger = logging.getLogger(__name__)

MAX_TODO_LENGTH = 140


@router.get("/todos", response_model=list[TodoSchema])
async def get_list() -> list[str]:
    return await TodoSchema.from_queryset(TodoModel.all())


@router.post("/todos", response_model=TodoSchema)
async def create(item: Annotated[str, Body(media_type="text/plain")]) -> str:
    if len(item) > MAX_TODO_LENGTH:
        logger.error(f"Too long todo {item}")
        raise HTTPException(status_code=400, detail="Too long")

    entry = await TodoModel.create(text=item)
    return await TodoSchema.from_tortoise_orm(entry)
