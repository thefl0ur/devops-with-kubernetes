from typing import Annotated

from fastapi import APIRouter, Body

router = APIRouter()

TODOS = ["Thing 1", "Thing 2", "Thing 3"]


@router.get("/todos")
async def get_list() -> list[str]:
    return TODOS


@router.post("/todos")
async def create(item: Annotated[str, Body(media_type="text/plain")]) -> str:
    TODOS.append(item)
    return item
