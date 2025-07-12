import os

from fastapi.responses import HTMLResponse
import uvicorn

from fastapi import FastAPI, Request


DEFAULT_PORT = 8000

app = FastAPI(name='TodoApp', docs_url=None, redoc_url=None, openapi_url=None)


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return """
    <html>
    <body>
    <p><h1>DVK ToDO app</h1></p>
    <body>
    </html>
"""


def start(port: int) -> None:
    print(f'Server started in port {port}')
    uvicorn.run(app, host='0.0.0.0', port=port)


def get_port() -> int:
    return int(os.getenv('PORT', DEFAULT_PORT))


if __name__ == '__main__':
    start(get_port())
