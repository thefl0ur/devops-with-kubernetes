import httpx


class TodoBackendService:
    def __init__(self):
        self._url = "http://todo-app-backend-service:2345/todos"
        # self._url = "http://localhost:8002/todos"

    async def _send_request(self, method: str, **kwargs) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.request(method, self._url, **kwargs)
        response.raise_for_status()

        return response

    async def load_data(self) -> list[str]:
        result = await self._send_request("GET")
        return result.json()

    async def insert(self, item: str) -> str:
        result = await self._send_request(
            "POST", content=item, headers={"Content-Type": "text/plain"}
        )
        return result.json()
