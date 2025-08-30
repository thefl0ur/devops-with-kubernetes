import uuid

from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from todo_app.config import IMAGE_NAME, TEMPLATES_DIR
from todo_app.tasks import update_image

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
async def root(request: Request, background_tasks: BackgroundTasks):
    context = {"request": request, "image_url": IMAGE_NAME, "uuid": uuid.uuid4().hex}

    background_tasks.add_task(update_image)
    return templates.TemplateResponse("index.jinja2", context)
