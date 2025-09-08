import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from todo_app.config import IMAGE_CACHE_DIR
from todo_app.routes import router
from todo_app.tasks import update_image

DEFAULT_PORT = 8001


@asynccontextmanager
async def lifespan(app: FastAPI):
    await update_image()
    yield


app = FastAPI(
    name="TodoApp", docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan
)
app.include_router(router)
app.mount("/static", StaticFiles(directory="todo_app/static"), name="static")
app.mount("/data", StaticFiles(directory=IMAGE_CACHE_DIR), name="data")

if __name__ == "__main__":
    port = int(os.getenv("PORT", DEFAULT_PORT))
    print(f"Server started in port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
