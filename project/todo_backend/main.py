import uvicorn
from fastapi import FastAPI

from todo_backend.config import settings
from todo_backend.routes import router

app = FastAPI(
    name="TodoAppBackend",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
app.include_router(router)

if __name__ == "__main__":
    print(f"Server started in port {settings.server_port}")
    uvicorn.run(app, host=settings.server_address, port=settings.server_port)
