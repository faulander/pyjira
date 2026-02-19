from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyjira.exceptions import raise_for_response
from pyjira.models.group import Group, GroupMembers

if TYPE_CHECKING:
    import httpx


class GroupResource:
    """Sync operations for Jira groups."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def create(self, name: str) -> Group:
        response = self._client.post(
            "/rest/api/3/group",
            json={"name": name},
        )
        raise_for_response(response)
        return Group.model_validate(response.json())

    def get(
        self,
        *,
        group_name: str | None = None,
        group_id: str | None = None,
    ) -> Group:
        params: dict[str, str] = {}
        if group_name:
            params["groupname"] = group_name
        if group_id:
            params["groupId"] = group_id
        response = self._client.get(
            "/rest/api/3/group",
            params=params,
        )
        raise_for_response(response)
        return Group.model_validate(response.json())

    def delete(
        self,
        *,
        group_name: str | None = None,
        group_id: str | None = None,
    ) -> None:
        params: dict[str, str] = {}
        if group_name:
            params["groupname"] = group_name
        if group_id:
            params["groupId"] = group_id
        response = self._client.delete(
            "/rest/api/3/group",
            params=params,
        )
        raise_for_response(response)

    def bulk_get(
        self,
        *,
        group_ids: list[str] | None = None,
        group_names: list[str] | None = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> dict[str, Any]:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if group_ids:
            params["groupId"] = ",".join(group_ids)
        if group_names:
            params["groupName"] = ",".join(group_names)
        response = self._client.get(
            "/rest/api/3/group/bulk",
            params=params,
        )
        raise_for_response(response)
        return response.json()

    def get_members(
        self,
        *,
        group_name: str | None = None,
        group_id: str | None = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> GroupMembers:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if group_name:
            params["groupname"] = group_name
        if group_id:
            params["groupId"] = group_id
        response = self._client.get(
            "/rest/api/3/group/member",
            params=params,
        )
        raise_for_response(response)
        return GroupMembers.model_validate(response.json())

    def add_user(
        self,
        *,
        group_name: str | None = None,
        group_id: str | None = None,
        account_id: str,
    ) -> Group:
        params: dict[str, str] = {}
        if group_name:
            params["groupname"] = group_name
        if group_id:
            params["groupId"] = group_id
        response = self._client.post(
            "/rest/api/3/group/user",
            params=params,
            json={"accountId": account_id},
        )
        raise_for_response(response)
        return Group.model_validate(response.json())

    def remove_user(
        self,
        *,
        group_name: str | None = None,
        group_id: str | None = None,
        account_id: str,
    ) -> None:
        params: dict[str, str] = {
            "accountId": account_id,
        }
        if group_name:
            params["groupname"] = group_name
        if group_id:
            params["groupId"] = group_id
        response = self._client.delete(
            "/rest/api/3/group/user",
            params=params,
        )
        raise_for_response(response)

    def find(self, query: str | None = None) -> list[Group]:
        params: dict[str, str] = {}
        if query:
            params["query"] = query
        response = self._client.get(
            "/rest/api/3/groups/picker",
            params=params,
        )
        raise_for_response(response)
        data = response.json()
        return [Group.model_validate(g) for g in data.get("groups", [])]


class AsyncGroupResource:
    """Async operations for Jira groups."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def create(self, name: str) -> Group:
        response = await self._client.post(
            "/rest/api/3/group",
            json={"name": name},
        )
        raise_for_response(response)
        return Group.model_validate(response.json())

    async def get(
        self,
        *,
        group_name: str | None = None,
        group_id: str | None = None,
    ) -> Group:
        params: dict[str, str] = {}
        if group_name:
            params["groupname"] = group_name
        if group_id:
            params["groupId"] = group_id
        response = await self._client.get(
            "/rest/api/3/group",
            params=params,
        )
        raise_for_response(response)
        return Group.model_validate(response.json())

    async def delete(
        self,
        *,
        group_name: str | None = None,
        group_id: str | None = None,
    ) -> None:
        params: dict[str, str] = {}
        if group_name:
            params["groupname"] = group_name
        if group_id:
            params["groupId"] = group_id
        response = await self._client.delete(
            "/rest/api/3/group",
            params=params,
        )
        raise_for_response(response)

    async def bulk_get(
        self,
        *,
        group_ids: list[str] | None = None,
        group_names: list[str] | None = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> dict[str, Any]:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if group_ids:
            params["groupId"] = ",".join(group_ids)
        if group_names:
            params["groupName"] = ",".join(group_names)
        response = await self._client.get(
            "/rest/api/3/group/bulk",
            params=params,
        )
        raise_for_response(response)
        return response.json()

    async def get_members(
        self,
        *,
        group_name: str | None = None,
        group_id: str | None = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> GroupMembers:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if group_name:
            params["groupname"] = group_name
        if group_id:
            params["groupId"] = group_id
        response = await self._client.get(
            "/rest/api/3/group/member",
            params=params,
        )
        raise_for_response(response)
        return GroupMembers.model_validate(response.json())

    async def add_user(
        self,
        *,
        group_name: str | None = None,
        group_id: str | None = None,
        account_id: str,
    ) -> Group:
        params: dict[str, str] = {}
        if group_name:
            params["groupname"] = group_name
        if group_id:
            params["groupId"] = group_id
        response = await self._client.post(
            "/rest/api/3/group/user",
            params=params,
            json={"accountId": account_id},
        )
        raise_for_response(response)
        return Group.model_validate(response.json())

    async def remove_user(
        self,
        *,
        group_name: str | None = None,
        group_id: str | None = None,
        account_id: str,
    ) -> None:
        params: dict[str, str] = {
            "accountId": account_id,
        }
        if group_name:
            params["groupname"] = group_name
        if group_id:
            params["groupId"] = group_id
        response = await self._client.delete(
            "/rest/api/3/group/user",
            params=params,
        )
        raise_for_response(response)

    async def find(self, query: str | None = None) -> list[Group]:
        params: dict[str, str] = {}
        if query:
            params["query"] = query
        response = await self._client.get(
            "/rest/api/3/groups/picker",
            params=params,
        )
        raise_for_response(response)
        data = response.json()
        return [Group.model_validate(g) for g in data.get("groups", [])]
