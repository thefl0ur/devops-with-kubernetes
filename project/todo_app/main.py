import os

import uvicorn

from fastapi import FastAPI


DEFAULT_PORT = 8000

app = FastAPI(name='TodoApp', docs_url=None, redoc_url=None, openapi_url=None)

def start(port: int) -> None:
    print(f'Server started in port {port}')
    uvicorn.run(app, port=port)

def get_port() -> int:
    return int(os.getenv('PORT', DEFAULT_PORT))

if __name__ == '__main__':
    start(get_port())

