from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyjira.exceptions import raise_for_response
from pyjira.models.field import FieldDetail, FieldPage

if TYPE_CHECKING:
    import httpx


class FieldResource:
    """Sync operations for Jira fields."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def list(self) -> list[FieldDetail]:
        response = self._client.get("/rest/api/3/field")
        raise_for_response(response)
        return [FieldDetail.model_validate(item) for item in response.json()]

    def search(
        self,
        *,
        start_at: int = 0,
        max_results: int = 50,
        type: list[str] | None = None,
        id: list[str] | None = None,
        query: str | None = None,
        order_by: str | None = None,
        expand: list[str] | None = None,
    ) -> FieldPage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if type:
            params["type"] = ",".join(type)
        if id:
            params["id"] = ",".join(id)
        if query:
            params["query"] = query
        if order_by:
            params["orderBy"] = order_by
        if expand:
            params["expand"] = ",".join(expand)
        response = self._client.get("/rest/api/3/field/search", params=params)
        raise_for_response(response)
        return FieldPage.model_validate(response.json())

    def search_trashed(
        self,
        *,
        start_at: int = 0,
        max_results: int = 50,
        id: list[str] | None = None,
        query: str | None = None,
        expand: list[str] | None = None,
        order_by: str | None = None,
    ) -> FieldPage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if id:
            params["id"] = ",".join(id)
        if query:
            params["query"] = query
        if expand:
            params["expand"] = ",".join(expand)
        if order_by:
            params["orderBy"] = order_by
        response = self._client.get(
            "/rest/api/3/field/search/trashed",
            params=params,
        )
        raise_for_response(response)
        return FieldPage.model_validate(response.json())

    def create(self, body: dict[str, Any]) -> FieldDetail:
        response = self._client.post("/rest/api/3/field", json=body)
        raise_for_response(response)
        return FieldDetail.model_validate(response.json())

    def update(self, field_id: str, body: dict[str, Any]) -> FieldDetail:
        response = self._client.put(
            f"/rest/api/3/field/{field_id}",
            json=body,
        )
        raise_for_response(response)
        return FieldDetail.model_validate(response.json())

    def delete(self, field_id: str) -> None:
        response = self._client.delete(f"/rest/api/3/field/{field_id}")
        raise_for_response(response)

    def trash(self, field_id: str) -> None:
        response = self._client.post(f"/rest/api/3/field/{field_id}/trash")
        raise_for_response(response)

    def restore(self, field_id: str) -> None:
        response = self._client.post(f"/rest/api/3/field/{field_id}/restore")
        raise_for_response(response)


class AsyncFieldResource:
    """Async operations for Jira fields."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def list(self) -> list[FieldDetail]:
        response = await self._client.get("/rest/api/3/field")
        raise_for_response(response)
        return [FieldDetail.model_validate(item) for item in response.json()]

    async def search(
        self,
        *,
        start_at: int = 0,
        max_results: int = 50,
        type: list[str] | None = None,
        id: list[str] | None = None,
        query: str | None = None,
        order_by: str | None = None,
        expand: list[str] | None = None,
    ) -> FieldPage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if type:
            params["type"] = ",".join(type)
        if id:
            params["id"] = ",".join(id)
        if query:
            params["query"] = query
        if order_by:
            params["orderBy"] = order_by
        if expand:
            params["expand"] = ",".join(expand)
        response = await self._client.get(
            "/rest/api/3/field/search",
            params=params,
        )
        raise_for_response(response)
        return FieldPage.model_validate(response.json())

    async def search_trashed(
        self,
        *,
        start_at: int = 0,
        max_results: int = 50,
        id: list[str] | None = None,
        query: str | None = None,
        expand: list[str] | None = None,
        order_by: str | None = None,
    ) -> FieldPage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if id:
            params["id"] = ",".join(id)
        if query:
            params["query"] = query
        if expand:
            params["expand"] = ",".join(expand)
        if order_by:
            params["orderBy"] = order_by
        response = await self._client.get(
            "/rest/api/3/field/search/trashed",
            params=params,
        )
        raise_for_response(response)
        return FieldPage.model_validate(response.json())

    async def create(self, body: dict[str, Any]) -> FieldDetail:
        response = await self._client.post("/rest/api/3/field", json=body)
        raise_for_response(response)
        return FieldDetail.model_validate(response.json())

    async def update(self, field_id: str, body: dict[str, Any]) -> FieldDetail:
        response = await self._client.put(
            f"/rest/api/3/field/{field_id}",
            json=body,
        )
        raise_for_response(response)
        return FieldDetail.model_validate(response.json())

    async def delete(self, field_id: str) -> None:
        response = await self._client.delete(f"/rest/api/3/field/{field_id}")
        raise_for_response(response)

    async def trash(self, field_id: str) -> None:
        response = await self._client.post(
            f"/rest/api/3/field/{field_id}/trash",
        )
        raise_for_response(response)

    async def restore(self, field_id: str) -> None:
        response = await self._client.post(
            f"/rest/api/3/field/{field_id}/restore",
        )
        raise_for_response(response)
