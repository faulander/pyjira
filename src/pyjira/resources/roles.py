from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyjira.exceptions import raise_for_response
from pyjira.models.role import ProjectRole

if TYPE_CHECKING:
    import httpx


class RoleResource:
    """Sync operations for Jira project roles."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def get_all(self) -> list[ProjectRole]:
        response = self._client.get("/rest/api/3/role")
        raise_for_response(response)
        return [ProjectRole.model_validate(r) for r in response.json()]

    def create(
        self,
        name: str,
        description: str | None = None,
    ) -> ProjectRole:
        payload: dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description
        response = self._client.post(
            "/rest/api/3/role",
            json=payload,
        )
        raise_for_response(response)
        return ProjectRole.model_validate(response.json())

    def get(self, role_id: str) -> ProjectRole:
        response = self._client.get(f"/rest/api/3/role/{role_id}")
        raise_for_response(response)
        return ProjectRole.model_validate(response.json())

    def update(self, role_id: str, body: dict[str, Any]) -> ProjectRole:
        response = self._client.put(
            f"/rest/api/3/role/{role_id}",
            json=body,
        )
        raise_for_response(response)
        return ProjectRole.model_validate(response.json())

    def partial_update(self, role_id: str, body: dict[str, Any]) -> ProjectRole:
        response = self._client.post(
            f"/rest/api/3/role/{role_id}",
            json=body,
        )
        raise_for_response(response)
        return ProjectRole.model_validate(response.json())

    def delete(
        self,
        role_id: str,
        *,
        swap_role_id: str | None = None,
    ) -> None:
        params: dict[str, str] = {}
        if swap_role_id:
            params["swap"] = swap_role_id
        response = self._client.delete(
            f"/rest/api/3/role/{role_id}",
            params=params,
        )
        raise_for_response(response)

    def get_default_actors(self, role_id: str) -> ProjectRole:
        response = self._client.get(
            f"/rest/api/3/role/{role_id}/actors",
        )
        raise_for_response(response)
        return ProjectRole.model_validate(response.json())

    def add_default_actors(
        self,
        role_id: str,
        body: dict[str, Any],
    ) -> ProjectRole:
        response = self._client.post(
            f"/rest/api/3/role/{role_id}/actors",
            json=body,
        )
        raise_for_response(response)
        return ProjectRole.model_validate(response.json())

    def remove_default_actors(
        self,
        role_id: str,
        *,
        user: str | None = None,
        group_id: str | None = None,
    ) -> ProjectRole:
        params: dict[str, str] = {}
        if user:
            params["user"] = user
        if group_id:
            params["groupId"] = group_id
        response = self._client.delete(
            f"/rest/api/3/role/{role_id}/actors",
            params=params,
        )
        raise_for_response(response)
        return ProjectRole.model_validate(response.json())


class AsyncRoleResource:
    """Async operations for Jira project roles."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def get_all(self) -> list[ProjectRole]:
        response = await self._client.get("/rest/api/3/role")
        raise_for_response(response)
        return [ProjectRole.model_validate(r) for r in response.json()]

    async def create(
        self,
        name: str,
        description: str | None = None,
    ) -> ProjectRole:
        payload: dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description
        response = await self._client.post(
            "/rest/api/3/role",
            json=payload,
        )
        raise_for_response(response)
        return ProjectRole.model_validate(response.json())

    async def get(self, role_id: str) -> ProjectRole:
        response = await self._client.get(f"/rest/api/3/role/{role_id}")
        raise_for_response(response)
        return ProjectRole.model_validate(response.json())

    async def update(self, role_id: str, body: dict[str, Any]) -> ProjectRole:
        response = await self._client.put(
            f"/rest/api/3/role/{role_id}",
            json=body,
        )
        raise_for_response(response)
        return ProjectRole.model_validate(response.json())

    async def partial_update(self, role_id: str, body: dict[str, Any]) -> ProjectRole:
        response = await self._client.post(
            f"/rest/api/3/role/{role_id}",
            json=body,
        )
        raise_for_response(response)
        return ProjectRole.model_validate(response.json())

    async def delete(
        self,
        role_id: str,
        *,
        swap_role_id: str | None = None,
    ) -> None:
        params: dict[str, str] = {}
        if swap_role_id:
            params["swap"] = swap_role_id
        response = await self._client.delete(
            f"/rest/api/3/role/{role_id}",
            params=params,
        )
        raise_for_response(response)

    async def get_default_actors(self, role_id: str) -> ProjectRole:
        response = await self._client.get(
            f"/rest/api/3/role/{role_id}/actors",
        )
        raise_for_response(response)
        return ProjectRole.model_validate(response.json())

    async def add_default_actors(
        self,
        role_id: str,
        body: dict[str, Any],
    ) -> ProjectRole:
        response = await self._client.post(
            f"/rest/api/3/role/{role_id}/actors",
            json=body,
        )
        raise_for_response(response)
        return ProjectRole.model_validate(response.json())

    async def remove_default_actors(
        self,
        role_id: str,
        *,
        user: str | None = None,
        group_id: str | None = None,
    ) -> ProjectRole:
        params: dict[str, str] = {}
        if user:
            params["user"] = user
        if group_id:
            params["groupId"] = group_id
        response = await self._client.delete(
            f"/rest/api/3/role/{role_id}/actors",
            params=params,
        )
        raise_for_response(response)
        return ProjectRole.model_validate(response.json())
