import uuid

from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Form, Header, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from todo_app.config import settings
from todo_app.dependencies import get_todo_service
from todo_app.services.todo_backend import TodoBackendService
from todo_app.tasks import update_image


router = APIRouter()

templates = Jinja2Templates(directory=settings.templates_dir)

TODOS = []


@router.get("/", response_class=HTMLResponse)
async def root(
    request: Request,
    background_tasks: BackgroundTasks,
    api_client: Annotated[TodoBackendService, Depends(get_todo_service)],
    hx_request: Annotated[str | None, Header()] = None,
):
    todos = await api_client.load_data()
    # Sort todos: incomplete first, then completed
    # Within each group, sort by ID descending (newest first)
    sorted_todos = sorted(
        todos, key=lambda x: (x.is_complete, -x.id if not x.is_complete else x.id)
    )

    if hx_request:
        return templates.TemplateResponse(
            request=request, name="todos.jinja2", context={"todos": sorted_todos}
        )

    context = {
        "request": request,
        "image_url": settings.image_name,
        "uuid": uuid.uuid4().hex,
        "todos": sorted_todos,
    }

    background_tasks.add_task(update_image)
    return templates.TemplateResponse("index.jinja2", context)


@router.post("/update/{todo_id}", response_class=HTMLResponse)
async def update(
    request: Request,
    todo_id: int,
    api_client: Annotated[TodoBackendService, Depends(get_todo_service)],
):
    await api_client.update(todo_id)
    # Load all todos to get the updated list
    all_todos = await api_client.load_data()
    # Sort todos: incomplete first, then completed
    # Within each group, sort by ID descending (newest first)
    sorted_todos = sorted(
        all_todos, key=lambda x: (x.is_complete, -x.id if not x.is_complete else x.id)
    )

    # Return the full sorted list
    return templates.TemplateResponse(
        request=request, name="todos.jinja2", context={"todos": sorted_todos}
    )


@router.post("/add", response_class=HTMLResponse)
async def create(
    request: Request,
    todo: Annotated[str, Form()],
    api_client: Annotated[TodoBackendService, Depends(get_todo_service)],
):
    created_todo = await api_client.insert(todo)
    # Load all todos to get the updated list
    all_todos = await api_client.load_data()
    # Sort todos: incomplete first, then completed
    # Within each group, sort by ID descending (newest first)
    sorted_todos = sorted(
        all_todos, key=lambda x: (x.is_complete, -x.id if not x.is_complete else x.id)
    )

    # Return the full sorted list
    return templates.TemplateResponse(
        request=request, name="todos.jinja2", context={"todos": sorted_todos}
    )
