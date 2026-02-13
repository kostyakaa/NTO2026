import httpx
from typing import Any, Dict


class NodeClient:
    def __init__(self, node_id: str, base_url: str = "http://127.0.0.1:8000"):
        self.node_id = node_id
        self.base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(base_url=self.base_url)

    async def send(self, recipient_id: str, payload: Dict[str, Any]):
        response = await self._client.post(
            "/send",
            json={
                "sender_id": self.node_id,
                "recipient_id": recipient_id,
                "payload": payload
            }
        )
        response.raise_for_status()
        return response.json()

    async def broadcast(self, payload: Dict[str, Any]):
        return await self.send("all", payload)

    async def read(self, long_polling: bool = False, timeout: int = 30):
        response = await self._client.get(
            "/read",
            params={
                "node_id": self.node_id,
                "long_polling": long_polling,
                "timeout": timeout
            }
        )
        response.raise_for_status()
        return response.json()["messages"]

    async def close(self):
        await self._client.aclose()
