from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyjira.exceptions import raise_for_response
from pyjira.models.component import Component, ComponentIssueCount

if TYPE_CHECKING:
    import httpx


class ComponentResource:
    """Sync operations for project components."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def create(self, body: dict[str, Any]) -> Component:
        response = self._client.post("/rest/api/3/component", json=body)
        raise_for_response(response)
        return Component.model_validate(response.json())

    def get(self, component_id: str) -> Component:
        response = self._client.get(f"/rest/api/3/component/{component_id}")
        raise_for_response(response)
        return Component.model_validate(response.json())

    def update(self, component_id: str, body: dict[str, Any]) -> Component:
        response = self._client.put(
            f"/rest/api/3/component/{component_id}",
            json=body,
        )
        raise_for_response(response)
        return Component.model_validate(response.json())

    def delete(
        self,
        component_id: str,
        *,
        move_issues_to: str | None = None,
    ) -> None:
        params: dict[str, str] = {}
        if move_issues_to is not None:
            params["moveIssuesTo"] = move_issues_to
        response = self._client.delete(
            f"/rest/api/3/component/{component_id}",
            params=params,
        )
        raise_for_response(response)

    def get_related_issue_count(
        self,
        component_id: str,
    ) -> ComponentIssueCount:
        response = self._client.get(
            f"/rest/api/3/component/{component_id}/relatedIssueCounts",
        )
        raise_for_response(response)
        return ComponentIssueCount.model_validate(response.json())

    def find_for_projects(
        self,
        *,
        project_ids: list[str],
        start_at: int = 0,
        max_results: int = 50,
    ) -> dict[str, Any]:
        params: dict[str, str] = {
            "projectIdsOrKeys": ",".join(project_ids),
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        response = self._client.get("/rest/api/3/component", params=params)
        raise_for_response(response)
        return response.json()


class AsyncComponentResource:
    """Async operations for project components."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def create(self, body: dict[str, Any]) -> Component:
        response = await self._client.post("/rest/api/3/component", json=body)
        raise_for_response(response)
        return Component.model_validate(response.json())

    async def get(self, component_id: str) -> Component:
        response = await self._client.get(
            f"/rest/api/3/component/{component_id}",
        )
        raise_for_response(response)
        return Component.model_validate(response.json())

    async def update(
        self,
        component_id: str,
        body: dict[str, Any],
    ) -> Component:
        response = await self._client.put(
            f"/rest/api/3/component/{component_id}",
            json=body,
        )
        raise_for_response(response)
        return Component.model_validate(response.json())

    async def delete(
        self,
        component_id: str,
        *,
        move_issues_to: str | None = None,
    ) -> None:
        params: dict[str, str] = {}
        if move_issues_to is not None:
            params["moveIssuesTo"] = move_issues_to
        response = await self._client.delete(
            f"/rest/api/3/component/{component_id}",
            params=params,
        )
        raise_for_response(response)

    async def get_related_issue_count(
        self,
        component_id: str,
    ) -> ComponentIssueCount:
        response = await self._client.get(
            f"/rest/api/3/component/{component_id}/relatedIssueCounts",
        )
        raise_for_response(response)
        return ComponentIssueCount.model_validate(response.json())

    async def find_for_projects(
        self,
        *,
        project_ids: list[str],
        start_at: int = 0,
        max_results: int = 50,
    ) -> dict[str, Any]:
        params: dict[str, str] = {
            "projectIdsOrKeys": ",".join(project_ids),
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        response = await self._client.get("/rest/api/3/component", params=params)
        raise_for_response(response)
        return response.json()
