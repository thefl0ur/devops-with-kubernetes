from typing import Annotated

from fastapi import APIRouter, Body

from todo_backend.handlers.schemas import TodoSchema
from todo_backend.models import TodoModel


router = APIRouter()


@router.get("/todos", response_model=list[TodoSchema])
async def get_list() -> list[str]:
    return await TodoSchema.from_queryset(TodoModel.all())


@router.post("/todos", response_model=TodoSchema)
async def create(item: Annotated[str, Body(media_type="text/plain")]) -> str:
    entry = await TodoModel.create(text=item)
    return await TodoSchema.from_tortoise_orm(entry)
