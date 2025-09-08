import os

import uvicorn
from fastapi import FastAPI

from todo_backend.routes import router

DEFAULT_PORT = 8001


app = FastAPI(
    name="TodoAppBackend",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
app.include_router(router)

if __name__ == "__main__":
    port = int(os.getenv("PORT", DEFAULT_PORT))
    print(f"Server started in port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
