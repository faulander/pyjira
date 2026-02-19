from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyjira.exceptions import raise_for_response
from pyjira.models.permission import PermissionGrant, PermissionScheme

if TYPE_CHECKING:
    import httpx


class PermissionResource:
    """Sync operations for Jira permissions."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def get_all(self) -> dict[str, Any]:
        response = self._client.get("/rest/api/3/permissions")
        raise_for_response(response)
        return response.json()

    def get_my_permissions(
        self,
        *,
        project_key: str | None = None,
        issue_key: str | None = None,
        permissions: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, str] = {}
        if project_key:
            params["projectKey"] = project_key
        if issue_key:
            params["issueKey"] = issue_key
        if permissions:
            params["permissions"] = permissions
        response = self._client.get(
            "/rest/api/3/mypermissions",
            params=params,
        )
        raise_for_response(response)
        return response.json()

    def get_all_schemes(
        self,
        *,
        expand: list[str] | None = None,
    ) -> list[PermissionScheme]:
        params: dict[str, str] = {}
        if expand:
            params["expand"] = ",".join(expand)
        response = self._client.get(
            "/rest/api/3/permissionscheme",
            params=params,
        )
        raise_for_response(response)
        data = response.json()
        return [
            PermissionScheme.model_validate(s)
            for s in data.get("permissionSchemes", [])
        ]

    def create_scheme(self, body: dict[str, Any]) -> PermissionScheme:
        response = self._client.post(
            "/rest/api/3/permissionscheme",
            json=body,
        )
        raise_for_response(response)
        return PermissionScheme.model_validate(response.json())

    def get_scheme(
        self,
        scheme_id: str,
        *,
        expand: list[str] | None = None,
    ) -> PermissionScheme:
        params: dict[str, str] = {}
        if expand:
            params["expand"] = ",".join(expand)
        response = self._client.get(
            f"/rest/api/3/permissionscheme/{scheme_id}",
            params=params,
        )
        raise_for_response(response)
        return PermissionScheme.model_validate(response.json())

    def update_scheme(
        self,
        scheme_id: str,
        body: dict[str, Any],
    ) -> PermissionScheme:
        response = self._client.put(
            f"/rest/api/3/permissionscheme/{scheme_id}",
            json=body,
        )
        raise_for_response(response)
        return PermissionScheme.model_validate(response.json())

    def delete_scheme(self, scheme_id: str) -> None:
        response = self._client.delete(
            f"/rest/api/3/permissionscheme/{scheme_id}",
        )
        raise_for_response(response)

    def get_scheme_grants(
        self,
        scheme_id: str,
        *,
        expand: list[str] | None = None,
    ) -> list[PermissionGrant]:
        params: dict[str, str] = {}
        if expand:
            params["expand"] = ",".join(expand)
        response = self._client.get(
            f"/rest/api/3/permissionscheme/{scheme_id}/permission",
            params=params,
        )
        raise_for_response(response)
        data = response.json()
        return [PermissionGrant.model_validate(g) for g in data.get("permissions", [])]

    def create_scheme_grant(
        self,
        scheme_id: str,
        body: dict[str, Any],
    ) -> PermissionGrant:
        response = self._client.post(
            f"/rest/api/3/permissionscheme/{scheme_id}/permission",
            json=body,
        )
        raise_for_response(response)
        return PermissionGrant.model_validate(response.json())

    def get_scheme_grant(
        self,
        scheme_id: str,
        permission_id: str,
    ) -> PermissionGrant:
        response = self._client.get(
            f"/rest/api/3/permissionscheme/{scheme_id}/permission/{permission_id}",
        )
        raise_for_response(response)
        return PermissionGrant.model_validate(response.json())

    def delete_scheme_grant(
        self,
        scheme_id: str,
        permission_id: str,
    ) -> None:
        response = self._client.delete(
            f"/rest/api/3/permissionscheme/{scheme_id}/permission/{permission_id}",
        )
        raise_for_response(response)


class AsyncPermissionResource:
    """Async operations for Jira permissions."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def get_all(self) -> dict[str, Any]:
        response = await self._client.get("/rest/api/3/permissions")
        raise_for_response(response)
        return response.json()

    async def get_my_permissions(
        self,
        *,
        project_key: str | None = None,
        issue_key: str | None = None,
        permissions: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, str] = {}
        if project_key:
            params["projectKey"] = project_key
        if issue_key:
            params["issueKey"] = issue_key
        if permissions:
            params["permissions"] = permissions
        response = await self._client.get(
            "/rest/api/3/mypermissions",
            params=params,
        )
        raise_for_response(response)
        return response.json()

    async def get_all_schemes(
        self,
        *,
        expand: list[str] | None = None,
    ) -> list[PermissionScheme]:
        params: dict[str, str] = {}
        if expand:
            params["expand"] = ",".join(expand)
        response = await self._client.get(
            "/rest/api/3/permissionscheme",
            params=params,
        )
        raise_for_response(response)
        data = response.json()
        return [
            PermissionScheme.model_validate(s)
            for s in data.get("permissionSchemes", [])
        ]

    async def create_scheme(self, body: dict[str, Any]) -> PermissionScheme:
        response = await self._client.post(
            "/rest/api/3/permissionscheme",
            json=body,
        )
        raise_for_response(response)
        return PermissionScheme.model_validate(response.json())

    async def get_scheme(
        self,
        scheme_id: str,
        *,
        expand: list[str] | None = None,
    ) -> PermissionScheme:
        params: dict[str, str] = {}
        if expand:
            params["expand"] = ",".join(expand)
        response = await self._client.get(
            f"/rest/api/3/permissionscheme/{scheme_id}",
            params=params,
        )
        raise_for_response(response)
        return PermissionScheme.model_validate(response.json())

    async def update_scheme(
        self,
        scheme_id: str,
        body: dict[str, Any],
    ) -> PermissionScheme:
        response = await self._client.put(
            f"/rest/api/3/permissionscheme/{scheme_id}",
            json=body,
        )
        raise_for_response(response)
        return PermissionScheme.model_validate(response.json())

    async def delete_scheme(self, scheme_id: str) -> None:
        response = await self._client.delete(
            f"/rest/api/3/permissionscheme/{scheme_id}",
        )
        raise_for_response(response)

    async def get_scheme_grants(
        self,
        scheme_id: str,
        *,
        expand: list[str] | None = None,
    ) -> list[PermissionGrant]:
        params: dict[str, str] = {}
        if expand:
            params["expand"] = ",".join(expand)
        response = await self._client.get(
            f"/rest/api/3/permissionscheme/{scheme_id}/permission",
            params=params,
        )
        raise_for_response(response)
        data = response.json()
        return [PermissionGrant.model_validate(g) for g in data.get("permissions", [])]

    async def create_scheme_grant(
        self,
        scheme_id: str,
        body: dict[str, Any],
    ) -> PermissionGrant:
        response = await self._client.post(
            f"/rest/api/3/permissionscheme/{scheme_id}/permission",
            json=body,
        )
        raise_for_response(response)
        return PermissionGrant.model_validate(response.json())

    async def get_scheme_grant(
        self,
        scheme_id: str,
        permission_id: str,
    ) -> PermissionGrant:
        response = await self._client.get(
            f"/rest/api/3/permissionscheme/{scheme_id}/permission/{permission_id}",
        )
        raise_for_response(response)
        return PermissionGrant.model_validate(response.json())

    async def delete_scheme_grant(
        self,
        scheme_id: str,
        permission_id: str,
    ) -> None:
        response = await self._client.delete(
            f"/rest/api/3/permissionscheme/{scheme_id}/permission/{permission_id}",
        )
        raise_for_response(response)
