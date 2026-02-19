from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyjira.exceptions import raise_for_response
from pyjira.models.priority_full import PriorityDetail, PriorityPage

if TYPE_CHECKING:
    import httpx


class PriorityResource:
    """Sync operations for issue priorities."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def list(self) -> list[PriorityDetail]:
        response = self._client.get("/rest/api/3/priority")
        raise_for_response(response)
        return [PriorityDetail.model_validate(item) for item in response.json()]

    def get(self, priority_id: str) -> PriorityDetail:
        response = self._client.get(f"/rest/api/3/priority/{priority_id}")
        raise_for_response(response)
        return PriorityDetail.model_validate(response.json())

    def search(
        self,
        *,
        start_at: int = 0,
        max_results: int = 50,
    ) -> PriorityPage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        response = self._client.get("/rest/api/3/priority/search", params=params)
        raise_for_response(response)
        return PriorityPage.model_validate(response.json())

    def create(self, body: dict[str, Any]) -> dict[str, Any]:
        response = self._client.post("/rest/api/3/priority", json=body)
        raise_for_response(response)
        return response.json()

    def update(self, priority_id: str, body: dict[str, Any]) -> None:
        response = self._client.put(
            f"/rest/api/3/priority/{priority_id}",
            json=body,
        )
        raise_for_response(response)

    def delete(self, priority_id: str, *, replace_with: str) -> None:
        params: dict[str, str] = {"replaceWith": replace_with}
        response = self._client.delete(
            f"/rest/api/3/priority/{priority_id}",
            params=params,
        )
        raise_for_response(response)

    def set_default(self, priority_id: str) -> None:
        response = self._client.put(
            "/rest/api/3/priority/default",
            json={"id": priority_id},
        )
        raise_for_response(response)

    def move(self, body: dict[str, Any]) -> None:
        response = self._client.put("/rest/api/3/priority/move", json=body)
        raise_for_response(response)


class AsyncPriorityResource:
    """Async operations for issue priorities."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def list(self) -> list[PriorityDetail]:
        response = await self._client.get("/rest/api/3/priority")
        raise_for_response(response)
        return [PriorityDetail.model_validate(item) for item in response.json()]

    async def get(self, priority_id: str) -> PriorityDetail:
        response = await self._client.get(f"/rest/api/3/priority/{priority_id}")
        raise_for_response(response)
        return PriorityDetail.model_validate(response.json())

    async def search(
        self,
        *,
        start_at: int = 0,
        max_results: int = 50,
    ) -> PriorityPage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        response = await self._client.get(
            "/rest/api/3/priority/search",
            params=params,
        )
        raise_for_response(response)
        return PriorityPage.model_validate(response.json())

    async def create(self, body: dict[str, Any]) -> dict[str, Any]:
        response = await self._client.post("/rest/api/3/priority", json=body)
        raise_for_response(response)
        return response.json()

    async def update(self, priority_id: str, body: dict[str, Any]) -> None:
        response = await self._client.put(
            f"/rest/api/3/priority/{priority_id}",
            json=body,
        )
        raise_for_response(response)

    async def delete(self, priority_id: str, *, replace_with: str) -> None:
        params: dict[str, str] = {"replaceWith": replace_with}
        response = await self._client.delete(
            f"/rest/api/3/priority/{priority_id}",
            params=params,
        )
        raise_for_response(response)

    async def set_default(self, priority_id: str) -> None:
        response = await self._client.put(
            "/rest/api/3/priority/default",
            json={"id": priority_id},
        )
        raise_for_response(response)

    async def move(self, body: dict[str, Any]) -> None:
        response = await self._client.put(
            "/rest/api/3/priority/move",
            json=body,
        )
        raise_for_response(response)
