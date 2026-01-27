import httpx

from pydantic import BaseModel
from pydantic.fields import Field

from todo_app.config import settings


class TodoModel(BaseModel):
    id: int
    text: str
    is_complete: bool = Field(default=False)

    class Config:
        # Allow aliasing of field names to match the backend API
        allow_population_by_field_name = True


class TodoBackendService:
    def __init__(self):
        self._url = settings.backend_address

    async def _send_request(self, method: str, url: str = None, **kwargs) -> httpx.Response:
        target_url = url if url is not None else self._url
        async with httpx.AsyncClient() as client:
            response = await client.request(method, target_url, **kwargs)
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

    async def update(self, todo_id: int) -> TodoModel:
        # Construct the URL for the specific todo item
        # settings.backend_address is like "http://backend:8001/todos"
        # We want to create "http://backend:8001/todos/{todo_id}"
        update_url = f"{self._url}/{todo_id}"

        result = await self._send_request(
            "PUT", headers={"Content-Type": "application/json"}, url=update_url
        )
        return TodoModel(**result.json())
