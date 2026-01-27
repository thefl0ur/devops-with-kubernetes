import logging

from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Request

from todo_backend.handlers.schemas import TodoSchema
from todo_backend.models import TodoModel


router = APIRouter()

logger = logging.getLogger(__name__)

MAX_TODO_LENGTH = 140


@router.get("/todos", response_model=list[TodoSchema])
async def get_list() -> list[str]:
    return await TodoSchema.from_queryset(TodoModel.all())


@router.post("/todos", response_model=TodoSchema)
async def create(request: Request, item: Annotated[str, Body(media_type="text/plain")]) -> str:
    if len(item) > MAX_TODO_LENGTH:
        logger.error(f"Too long todo {item}")
        raise HTTPException(status_code=400, detail="Too long")

    entry = await TodoModel.create(text=item)
    schema = await TodoSchema.from_tortoise_orm(entry)
    logger.info(f"Task id {entry.id} created successfully: {entry.text}")

    # Publish event to NATS if publisher is available
    nats_publisher = getattr(request.app.state, "nats_publisher", None)
    if nats_publisher:
        logger.info("Publish CREATE")
        await nats_publisher.publish_todo_event("created", schema.model_dump())

    return schema


@router.put("/todos/{todo_id}", response_model=TodoSchema)
async def update_todo(request: Request, todo_id: int) -> TodoSchema:
    todo = await TodoModel.get_or_none(id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.is_complete = True
    await todo.save()

    schema = await TodoSchema.from_tortoise_orm(todo)

    # Publish event to NATS if publisher is available
    nats_publisher = getattr(request.app.state, "nats_publisher", None)
    if nats_publisher:
        logger.info("Publish UPDATE")
        await nats_publisher.publish_todo_event("updated", schema.model_dump())

    return schema
