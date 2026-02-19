from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyjira.exceptions import raise_for_response
from pyjira.models.status_full import StatusDetail, StatusPage

if TYPE_CHECKING:
    import httpx


class StatusResource:
    """Sync operations for issue statuses."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def get(
        self,
        *,
        ids: list[str] | None = None,
        expand: list[str] | None = None,
    ) -> list[StatusDetail]:
        params: dict[str, str] = {}
        if ids:
            params["id"] = ",".join(ids)
        if expand:
            params["expand"] = ",".join(expand)
        response = self._client.get("/rest/api/3/statuses", params=params)
        raise_for_response(response)
        return [StatusDetail.model_validate(item) for item in response.json()]

    def search(
        self,
        *,
        search_string: str | None = None,
        start_at: int = 0,
        max_results: int = 50,
        expand: list[str] | None = None,
    ) -> StatusPage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if search_string:
            params["searchString"] = search_string
        if expand:
            params["expand"] = ",".join(expand)
        response = self._client.get("/rest/api/3/statuses/search", params=params)
        raise_for_response(response)
        return StatusPage.model_validate(response.json())

    def create(self, body: dict[str, Any]) -> list[StatusDetail]:
        response = self._client.post("/rest/api/3/statuses", json=body)
        raise_for_response(response)
        return [StatusDetail.model_validate(item) for item in response.json()]

    def update(self, body: dict[str, Any]) -> None:
        response = self._client.put("/rest/api/3/statuses", json=body)
        raise_for_response(response)

    def delete(self, *, ids: list[str]) -> None:
        params: dict[str, str] = {"id": ",".join(ids)}
        response = self._client.delete("/rest/api/3/statuses", params=params)
        raise_for_response(response)


class AsyncStatusResource:
    """Async operations for issue statuses."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def get(
        self,
        *,
        ids: list[str] | None = None,
        expand: list[str] | None = None,
    ) -> list[StatusDetail]:
        params: dict[str, str] = {}
        if ids:
            params["id"] = ",".join(ids)
        if expand:
            params["expand"] = ",".join(expand)
        response = await self._client.get("/rest/api/3/statuses", params=params)
        raise_for_response(response)
        return [StatusDetail.model_validate(item) for item in response.json()]

    async def search(
        self,
        *,
        search_string: str | None = None,
        start_at: int = 0,
        max_results: int = 50,
        expand: list[str] | None = None,
    ) -> StatusPage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if search_string:
            params["searchString"] = search_string
        if expand:
            params["expand"] = ",".join(expand)
        response = await self._client.get(
            "/rest/api/3/statuses/search",
            params=params,
        )
        raise_for_response(response)
        return StatusPage.model_validate(response.json())

    async def create(self, body: dict[str, Any]) -> list[StatusDetail]:
        response = await self._client.post("/rest/api/3/statuses", json=body)
        raise_for_response(response)
        return [StatusDetail.model_validate(item) for item in response.json()]

    async def update(self, body: dict[str, Any]) -> None:
        response = await self._client.put("/rest/api/3/statuses", json=body)
        raise_for_response(response)

    async def delete(self, *, ids: list[str]) -> None:
        params: dict[str, str] = {"id": ",".join(ids)}
        response = await self._client.delete(
            "/rest/api/3/statuses",
            params=params,
        )
        raise_for_response(response)
