import logging

from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise

from todo_backend.config import settings
from todo_backend.publisher import NatsPublisher
from todo_backend.routes import router


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    nats_publisher = None
    if settings.nats_url:
        nats_publisher = NatsPublisher(settings.nats_url)
        await nats_publisher.connect()

    app.state.nats_publisher = nats_publisher

    async with RegisterTortoise(
        app,
        db_url=settings.db_connections_string,
        modules={"models": ["todo_backend.models"]},
        generate_schemas=True,
    ):
        yield

    if nats_publisher and nats_publisher.nc:
        await nats_publisher.nc.close()


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
