from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyjira.exceptions import raise_for_response
from pyjira.models.issuetype_full import IssueTypeDetail

if TYPE_CHECKING:
    import httpx


class IssueTypeResource:
    """Sync operations for Jira issue types."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def list(self) -> list[IssueTypeDetail]:
        response = self._client.get("/rest/api/3/issuetype")
        raise_for_response(response)
        return [IssueTypeDetail.model_validate(item) for item in response.json()]

    def get(self, issue_type_id: str) -> IssueTypeDetail:
        response = self._client.get(f"/rest/api/3/issuetype/{issue_type_id}")
        raise_for_response(response)
        return IssueTypeDetail.model_validate(response.json())

    def create(self, body: dict[str, Any]) -> IssueTypeDetail:
        response = self._client.post("/rest/api/3/issuetype", json=body)
        raise_for_response(response)
        return IssueTypeDetail.model_validate(response.json())

    def update(
        self,
        issue_type_id: str,
        body: dict[str, Any],
    ) -> IssueTypeDetail:
        response = self._client.put(
            f"/rest/api/3/issuetype/{issue_type_id}",
            json=body,
        )
        raise_for_response(response)
        return IssueTypeDetail.model_validate(response.json())

    def delete(
        self,
        issue_type_id: str,
        *,
        alternative_issue_type_id: str | None = None,
    ) -> None:
        params: dict[str, str] = {}
        if alternative_issue_type_id:
            params["alternativeIssueTypeId"] = alternative_issue_type_id
        response = self._client.delete(
            f"/rest/api/3/issuetype/{issue_type_id}",
            params=params,
        )
        raise_for_response(response)

    def get_for_project(
        self,
        project_id_or_key: str,
        *,
        level: int | None = None,
    ) -> list[IssueTypeDetail]:
        params: dict[str, str] = {"projectId": project_id_or_key}
        if level is not None:
            params["level"] = str(level)
        response = self._client.get(
            "/rest/api/3/issuetype/project",
            params=params,
        )
        raise_for_response(response)
        return [IssueTypeDetail.model_validate(item) for item in response.json()]

    def get_alternatives(
        self,
        issue_type_id: str,
    ) -> list[IssueTypeDetail]:
        response = self._client.get(
            f"/rest/api/3/issuetype/{issue_type_id}/alternatives",
        )
        raise_for_response(response)
        return [IssueTypeDetail.model_validate(item) for item in response.json()]

    def get_property_keys(self, issue_type_id: str) -> list[dict[str, Any]]:
        response = self._client.get(
            f"/rest/api/3/issuetype/{issue_type_id}/properties",
        )
        raise_for_response(response)
        data = response.json()
        return data.get("keys", [])

    def get_property(
        self,
        issue_type_id: str,
        property_key: str,
    ) -> dict[str, Any]:
        response = self._client.get(
            f"/rest/api/3/issuetype/{issue_type_id}/properties/{property_key}",
        )
        raise_for_response(response)
        return response.json()

    def set_property(
        self,
        issue_type_id: str,
        property_key: str,
        value: Any,
    ) -> None:
        response = self._client.put(
            f"/rest/api/3/issuetype/{issue_type_id}/properties/{property_key}",
            json=value,
        )
        raise_for_response(response)

    def delete_property(
        self,
        issue_type_id: str,
        property_key: str,
    ) -> None:
        response = self._client.delete(
            f"/rest/api/3/issuetype/{issue_type_id}/properties/{property_key}",
        )
        raise_for_response(response)


class AsyncIssueTypeResource:
    """Async operations for Jira issue types."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def list(self) -> list[IssueTypeDetail]:
        response = await self._client.get("/rest/api/3/issuetype")
        raise_for_response(response)
        return [IssueTypeDetail.model_validate(item) for item in response.json()]

    async def get(self, issue_type_id: str) -> IssueTypeDetail:
        response = await self._client.get(
            f"/rest/api/3/issuetype/{issue_type_id}",
        )
        raise_for_response(response)
        return IssueTypeDetail.model_validate(response.json())

    async def create(self, body: dict[str, Any]) -> IssueTypeDetail:
        response = await self._client.post("/rest/api/3/issuetype", json=body)
        raise_for_response(response)
        return IssueTypeDetail.model_validate(response.json())

    async def update(
        self,
        issue_type_id: str,
        body: dict[str, Any],
    ) -> IssueTypeDetail:
        response = await self._client.put(
            f"/rest/api/3/issuetype/{issue_type_id}",
            json=body,
        )
        raise_for_response(response)
        return IssueTypeDetail.model_validate(response.json())

    async def delete(
        self,
        issue_type_id: str,
        *,
        alternative_issue_type_id: str | None = None,
    ) -> None:
        params: dict[str, str] = {}
        if alternative_issue_type_id:
            params["alternativeIssueTypeId"] = alternative_issue_type_id
        response = await self._client.delete(
            f"/rest/api/3/issuetype/{issue_type_id}",
            params=params,
        )
        raise_for_response(response)

    async def get_for_project(
        self,
        project_id_or_key: str,
        *,
        level: int | None = None,
    ) -> list[IssueTypeDetail]:
        params: dict[str, str] = {"projectId": project_id_or_key}
        if level is not None:
            params["level"] = str(level)
        response = await self._client.get(
            "/rest/api/3/issuetype/project",
            params=params,
        )
        raise_for_response(response)
        return [IssueTypeDetail.model_validate(item) for item in response.json()]

    async def get_alternatives(
        self,
        issue_type_id: str,
    ) -> list[IssueTypeDetail]:
        response = await self._client.get(
            f"/rest/api/3/issuetype/{issue_type_id}/alternatives",
        )
        raise_for_response(response)
        return [IssueTypeDetail.model_validate(item) for item in response.json()]

    async def get_property_keys(
        self,
        issue_type_id: str,
    ) -> list[dict[str, Any]]:
        response = await self._client.get(
            f"/rest/api/3/issuetype/{issue_type_id}/properties",
        )
        raise_for_response(response)
        data = response.json()
        return data.get("keys", [])

    async def get_property(
        self,
        issue_type_id: str,
        property_key: str,
    ) -> dict[str, Any]:
        response = await self._client.get(
            f"/rest/api/3/issuetype/{issue_type_id}/properties/{property_key}",
        )
        raise_for_response(response)
        return response.json()

    async def set_property(
        self,
        issue_type_id: str,
        property_key: str,
        value: Any,
    ) -> None:
        response = await self._client.put(
            f"/rest/api/3/issuetype/{issue_type_id}/properties/{property_key}",
            json=value,
        )
        raise_for_response(response)

    async def delete_property(
        self,
        issue_type_id: str,
        property_key: str,
    ) -> None:
        response = await self._client.delete(
            f"/rest/api/3/issuetype/{issue_type_id}/properties/{property_key}",
        )
        raise_for_response(response)
