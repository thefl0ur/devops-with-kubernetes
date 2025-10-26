import httpx

from pydantic import BaseModel

from todo_app.config import settings


class TodoModel(BaseModel):
    id: int
    text: str
    is_completed: bool = False


class TodoBackendService:
    def __init__(self):
        self._url = settings.backend_address

    async def _send_request(self, method: str, **kwargs) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.request(method, self._url, **kwargs)
        response.raise_for_status()

        return response

    async def load_data(self) -> list[TodoModel]:
        result = await self._send_request("GET")
        return [TodoModel(**x) for x in result.json()]

    async def insert(self, item: str) -> TodoModel:
        result = await self._send_request(
            "POST", content=item, headers={"Content-Type": "text/plain"}
        )
        return TodoModel(**result.json())
