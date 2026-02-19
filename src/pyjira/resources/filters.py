from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyjira.exceptions import raise_for_response
from pyjira.models.filter import Filter, FilterPage, SharePermission

if TYPE_CHECKING:
    import httpx


class FilterResource:
    """Sync operations for Jira filters."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def create(self, body: dict[str, Any]) -> Filter:
        response = self._client.post("/rest/api/3/filter", json=body)
        raise_for_response(response)
        return Filter.model_validate(response.json())

    def get(self, filter_id: str) -> Filter:
        response = self._client.get(f"/rest/api/3/filter/{filter_id}")
        raise_for_response(response)
        return Filter.model_validate(response.json())

    def update(self, filter_id: str, body: dict[str, Any]) -> Filter:
        response = self._client.put(
            f"/rest/api/3/filter/{filter_id}",
            json=body,
        )
        raise_for_response(response)
        return Filter.model_validate(response.json())

    def delete(self, filter_id: str) -> None:
        response = self._client.delete(f"/rest/api/3/filter/{filter_id}")
        raise_for_response(response)

    def search(
        self,
        *,
        filter_name: str | None = None,
        expand: list[str] | None = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> FilterPage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if filter_name:
            params["filterName"] = filter_name
        if expand:
            params["expand"] = ",".join(expand)
        response = self._client.get(
            "/rest/api/3/filter/search",
            params=params,
        )
        raise_for_response(response)
        return FilterPage.model_validate(response.json())

    def get_favourites(
        self,
        *,
        expand: list[str] | None = None,
    ) -> list[Filter]:
        params: dict[str, str] = {}
        if expand:
            params["expand"] = ",".join(expand)
        response = self._client.get(
            "/rest/api/3/filter/favourite",
            params=params,
        )
        raise_for_response(response)
        return [Filter.model_validate(f) for f in response.json()]

    def get_my_filters(
        self,
        *,
        expand: list[str] | None = None,
    ) -> list[Filter]:
        params: dict[str, str] = {}
        if expand:
            params["expand"] = ",".join(expand)
        response = self._client.get(
            "/rest/api/3/filter/my",
            params=params,
        )
        raise_for_response(response)
        return [Filter.model_validate(f) for f in response.json()]

    def set_favourite(self, filter_id: str) -> Filter:
        response = self._client.put(
            f"/rest/api/3/filter/{filter_id}/favourite",
        )
        raise_for_response(response)
        return Filter.model_validate(response.json())

    def remove_favourite(self, filter_id: str) -> None:
        response = self._client.delete(
            f"/rest/api/3/filter/{filter_id}/favourite",
        )
        raise_for_response(response)

    def get_share_permissions(
        self,
        filter_id: str,
    ) -> list[SharePermission]:
        response = self._client.get(
            f"/rest/api/3/filter/{filter_id}/permission",
        )
        raise_for_response(response)
        return [SharePermission.model_validate(p) for p in response.json()]

    def add_share_permission(
        self,
        filter_id: str,
        body: dict[str, Any],
    ) -> list[SharePermission]:
        response = self._client.post(
            f"/rest/api/3/filter/{filter_id}/permission",
            json=body,
        )
        raise_for_response(response)
        return [SharePermission.model_validate(p) for p in response.json()]

    def delete_share_permission(
        self,
        filter_id: str,
        permission_id: str,
    ) -> None:
        response = self._client.delete(
            f"/rest/api/3/filter/{filter_id}/permission/{permission_id}",
        )
        raise_for_response(response)

    def change_owner(self, filter_id: str, account_id: str) -> None:
        response = self._client.put(
            f"/rest/api/3/filter/{filter_id}/owner",
            json={"accountId": account_id},
        )
        raise_for_response(response)


class AsyncFilterResource:
    """Async operations for Jira filters."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def create(self, body: dict[str, Any]) -> Filter:
        response = await self._client.post("/rest/api/3/filter", json=body)
        raise_for_response(response)
        return Filter.model_validate(response.json())

    async def get(self, filter_id: str) -> Filter:
        response = await self._client.get(
            f"/rest/api/3/filter/{filter_id}",
        )
        raise_for_response(response)
        return Filter.model_validate(response.json())

    async def update(
        self,
        filter_id: str,
        body: dict[str, Any],
    ) -> Filter:
        response = await self._client.put(
            f"/rest/api/3/filter/{filter_id}",
            json=body,
        )
        raise_for_response(response)
        return Filter.model_validate(response.json())

    async def delete(self, filter_id: str) -> None:
        response = await self._client.delete(
            f"/rest/api/3/filter/{filter_id}",
        )
        raise_for_response(response)

    async def search(
        self,
        *,
        filter_name: str | None = None,
        expand: list[str] | None = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> FilterPage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if filter_name:
            params["filterName"] = filter_name
        if expand:
            params["expand"] = ",".join(expand)
        response = await self._client.get(
            "/rest/api/3/filter/search",
            params=params,
        )
        raise_for_response(response)
        return FilterPage.model_validate(response.json())

    async def get_favourites(
        self,
        *,
        expand: list[str] | None = None,
    ) -> list[Filter]:
        params: dict[str, str] = {}
        if expand:
            params["expand"] = ",".join(expand)
        response = await self._client.get(
            "/rest/api/3/filter/favourite",
            params=params,
        )
        raise_for_response(response)
        return [Filter.model_validate(f) for f in response.json()]

    async def get_my_filters(
        self,
        *,
        expand: list[str] | None = None,
    ) -> list[Filter]:
        params: dict[str, str] = {}
        if expand:
            params["expand"] = ",".join(expand)
        response = await self._client.get(
            "/rest/api/3/filter/my",
            params=params,
        )
        raise_for_response(response)
        return [Filter.model_validate(f) for f in response.json()]

    async def set_favourite(self, filter_id: str) -> Filter:
        response = await self._client.put(
            f"/rest/api/3/filter/{filter_id}/favourite",
        )
        raise_for_response(response)
        return Filter.model_validate(response.json())

    async def remove_favourite(self, filter_id: str) -> None:
        response = await self._client.delete(
            f"/rest/api/3/filter/{filter_id}/favourite",
        )
        raise_for_response(response)

    async def get_share_permissions(
        self,
        filter_id: str,
    ) -> list[SharePermission]:
        response = await self._client.get(
            f"/rest/api/3/filter/{filter_id}/permission",
        )
        raise_for_response(response)
        return [SharePermission.model_validate(p) for p in response.json()]

    async def add_share_permission(
        self,
        filter_id: str,
        body: dict[str, Any],
    ) -> list[SharePermission]:
        response = await self._client.post(
            f"/rest/api/3/filter/{filter_id}/permission",
            json=body,
        )
        raise_for_response(response)
        return [SharePermission.model_validate(p) for p in response.json()]

    async def delete_share_permission(
        self,
        filter_id: str,
        permission_id: str,
    ) -> None:
        response = await self._client.delete(
            f"/rest/api/3/filter/{filter_id}/permission/{permission_id}",
        )
        raise_for_response(response)

    async def change_owner(
        self,
        filter_id: str,
        account_id: str,
    ) -> None:
        response = await self._client.put(
            f"/rest/api/3/filter/{filter_id}/owner",
            json={"accountId": account_id},
        )
        raise_for_response(response)
