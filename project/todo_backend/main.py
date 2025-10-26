from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise

from todo_backend.config import settings
from todo_backend.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with RegisterTortoise(
        app,
        db_url=settings.db_connections_string,
        modules={"models": ["todo_backend.models"]},
        generate_schemas=True,
    ):
        yield


app = FastAPI(
    name="TodoAppBackend",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
app.include_router(router)

if __name__ == "__main__":
    print(f"Server started in port {settings.server_port}")  # noqa
    uvicorn.run(app, host=settings.server_address, port=settings.server_port)
