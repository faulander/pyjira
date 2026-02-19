from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyjira.exceptions import raise_for_response
from pyjira.models.version import Version

if TYPE_CHECKING:
    import httpx


class VersionResource:
    """Sync operations for project versions."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def create(self, body: dict[str, Any]) -> Version:
        response = self._client.post("/rest/api/3/version", json=body)
        raise_for_response(response)
        return Version.model_validate(response.json())

    def get(self, version_id: str) -> Version:
        response = self._client.get(f"/rest/api/3/version/{version_id}")
        raise_for_response(response)
        return Version.model_validate(response.json())

    def update(self, version_id: str, body: dict[str, Any]) -> Version:
        response = self._client.put(
            f"/rest/api/3/version/{version_id}",
            json=body,
        )
        raise_for_response(response)
        return Version.model_validate(response.json())

    def delete(
        self,
        version_id: str,
        *,
        move_fix_issues_to: str | None = None,
        move_affected_issues_to: str | None = None,
    ) -> None:
        params: dict[str, str] = {}
        if move_fix_issues_to is not None:
            params["moveFixIssuesTo"] = move_fix_issues_to
        if move_affected_issues_to is not None:
            params["moveAffectedIssuesTo"] = move_affected_issues_to
        response = self._client.delete(
            f"/rest/api/3/version/{version_id}",
            params=params,
        )
        raise_for_response(response)

    def merge(self, version_id: str, move_issues_to_id: str) -> None:
        response = self._client.put(
            f"/rest/api/3/version/{version_id}/mergeto/{move_issues_to_id}",
        )
        raise_for_response(response)

    def move(self, version_id: str, body: dict[str, Any]) -> Version:
        response = self._client.post(
            f"/rest/api/3/version/{version_id}/move",
            json=body,
        )
        raise_for_response(response)
        return Version.model_validate(response.json())

    def get_related_issue_counts(self, version_id: str) -> dict[str, Any]:
        response = self._client.get(
            f"/rest/api/3/version/{version_id}/relatedIssueCounts",
        )
        raise_for_response(response)
        return response.json()

    def get_unresolved_issue_count(self, version_id: str) -> dict[str, Any]:
        response = self._client.get(
            f"/rest/api/3/version/{version_id}/unresolvedIssueCount",
        )
        raise_for_response(response)
        return response.json()


class AsyncVersionResource:
    """Async operations for project versions."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def create(self, body: dict[str, Any]) -> Version:
        response = await self._client.post("/rest/api/3/version", json=body)
        raise_for_response(response)
        return Version.model_validate(response.json())

    async def get(self, version_id: str) -> Version:
        response = await self._client.get(f"/rest/api/3/version/{version_id}")
        raise_for_response(response)
        return Version.model_validate(response.json())

    async def update(self, version_id: str, body: dict[str, Any]) -> Version:
        response = await self._client.put(
            f"/rest/api/3/version/{version_id}",
            json=body,
        )
        raise_for_response(response)
        return Version.model_validate(response.json())

    async def delete(
        self,
        version_id: str,
        *,
        move_fix_issues_to: str | None = None,
        move_affected_issues_to: str | None = None,
    ) -> None:
        params: dict[str, str] = {}
        if move_fix_issues_to is not None:
            params["moveFixIssuesTo"] = move_fix_issues_to
        if move_affected_issues_to is not None:
            params["moveAffectedIssuesTo"] = move_affected_issues_to
        response = await self._client.delete(
            f"/rest/api/3/version/{version_id}",
            params=params,
        )
        raise_for_response(response)

    async def merge(self, version_id: str, move_issues_to_id: str) -> None:
        response = await self._client.put(
            f"/rest/api/3/version/{version_id}/mergeto/{move_issues_to_id}",
        )
        raise_for_response(response)

    async def move(self, version_id: str, body: dict[str, Any]) -> Version:
        response = await self._client.post(
            f"/rest/api/3/version/{version_id}/move",
            json=body,
        )
        raise_for_response(response)
        return Version.model_validate(response.json())

    async def get_related_issue_counts(self, version_id: str) -> dict[str, Any]:
        response = await self._client.get(
            f"/rest/api/3/version/{version_id}/relatedIssueCounts",
        )
        raise_for_response(response)
        return response.json()

    async def get_unresolved_issue_count(self, version_id: str) -> dict[str, Any]:
        response = await self._client.get(
            f"/rest/api/3/version/{version_id}/unresolvedIssueCount",
        )
        raise_for_response(response)
        return response.json()
