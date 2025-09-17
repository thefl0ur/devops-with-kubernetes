from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from todo_app.config import settings
from todo_app.routes import router
from todo_app.tasks import update_image


@asynccontextmanager
async def lifespan(_: FastAPI):
    await update_image()
    yield


app = FastAPI(
    name="TodoApp", docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan
)
app.include_router(router)
app.mount("/static", StaticFiles(directory="todo_app/static"), name="static")
app.mount("/data", StaticFiles(directory=settings.image_cache_folder), name="data")

if __name__ == "__main__":
    print(f"Server started in port {settings.server_port}")
    uvicorn.run(app, host=settings.server_address, port=settings.server_port)
