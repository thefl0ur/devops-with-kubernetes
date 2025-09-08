import uuid
from typing import Annotated, Union

from fastapi import APIRouter, BackgroundTasks, Depends, Form, Header, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from todo_app.config import IMAGE_NAME, TEMPLATES_DIR
from todo_app.dependencies import get_todo_service
from todo_app.services.todo_backend import TodoBackendService
from todo_app.tasks import update_image

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)

TODOS = []


@router.get("/", response_class=HTMLResponse)
async def root(
    request: Request,
    background_tasks: BackgroundTasks,
    api_client: Annotated[TodoBackendService, Depends(get_todo_service)],
    hx_request: Annotated[str | None, Header()] = None,
):
    todos = await api_client.load_data()
    if hx_request:
        return templates.TemplateResponse(
            request=request, name="todos.jinja2", context={"todos": todos}
        )

    context = {
        "request": request,
        "image_url": IMAGE_NAME,
        "uuid": uuid.uuid4().hex,
        "todos": TODOS,
    }

    background_tasks.add_task(update_image)
    return templates.TemplateResponse("index.jinja2", context)


@router.post("/add", response_class=HTMLResponse)
async def create(
    request: Request,
    todo: Annotated[str, Form()],
    api_client: Annotated[TodoBackendService, Depends(get_todo_service)],
):
    created_todo = await api_client.insert(todo)
    return templates.TemplateResponse(
        request=request, name="todos.jinja2", context={"todos": [created_todo]}
    )
