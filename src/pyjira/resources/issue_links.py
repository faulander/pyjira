from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyjira.exceptions import raise_for_response
from pyjira.models.issue_link import IssueLink, IssueLinkType

if TYPE_CHECKING:
    import httpx


class IssueLinkResource:
    """Sync operations for issue links and link types."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def link(
        self,
        type: dict[str, Any],
        inward_issue: dict[str, Any],
        outward_issue: dict[str, Any],
        *,
        comment: dict[str, Any] | None = None,
    ) -> None:
        payload: dict[str, Any] = {
            "type": type,
            "inwardIssue": inward_issue,
            "outwardIssue": outward_issue,
        }
        if comment:
            payload["comment"] = comment
        response = self._client.post(
            "/rest/api/3/issueLink",
            json=payload,
        )
        raise_for_response(response)

    def get(self, link_id: str) -> IssueLink:
        response = self._client.get(
            f"/rest/api/3/issueLink/{link_id}",
        )
        raise_for_response(response)
        return IssueLink.model_validate(response.json())

    def delete(self, link_id: str) -> None:
        response = self._client.delete(
            f"/rest/api/3/issueLink/{link_id}",
        )
        raise_for_response(response)

    def get_link_types(self) -> list[IssueLinkType]:
        response = self._client.get(
            "/rest/api/3/issueLinkType",
        )
        raise_for_response(response)
        data = response.json()
        return [
            IssueLinkType.model_validate(item)
            for item in data.get("issueLinkTypes", [])
        ]

    def get_link_type(self, link_type_id: str) -> IssueLinkType:
        response = self._client.get(
            f"/rest/api/3/issueLinkType/{link_type_id}",
        )
        raise_for_response(response)
        return IssueLinkType.model_validate(response.json())

    def create_link_type(
        self,
        name: str,
        inward: str,
        outward: str,
    ) -> IssueLinkType:
        payload: dict[str, str] = {
            "name": name,
            "inward": inward,
            "outward": outward,
        }
        response = self._client.post(
            "/rest/api/3/issueLinkType",
            json=payload,
        )
        raise_for_response(response)
        return IssueLinkType.model_validate(response.json())

    def update_link_type(
        self,
        link_type_id: str,
        name: str,
        inward: str,
        outward: str,
    ) -> IssueLinkType:
        payload: dict[str, str] = {
            "name": name,
            "inward": inward,
            "outward": outward,
        }
        response = self._client.put(
            f"/rest/api/3/issueLinkType/{link_type_id}",
            json=payload,
        )
        raise_for_response(response)
        return IssueLinkType.model_validate(response.json())

    def delete_link_type(self, link_type_id: str) -> None:
        response = self._client.delete(
            f"/rest/api/3/issueLinkType/{link_type_id}",
        )
        raise_for_response(response)


class AsyncIssueLinkResource:
    """Async operations for issue links and link types."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def link(
        self,
        type: dict[str, Any],
        inward_issue: dict[str, Any],
        outward_issue: dict[str, Any],
        *,
        comment: dict[str, Any] | None = None,
    ) -> None:
        payload: dict[str, Any] = {
            "type": type,
            "inwardIssue": inward_issue,
            "outwardIssue": outward_issue,
        }
        if comment:
            payload["comment"] = comment
        response = await self._client.post(
            "/rest/api/3/issueLink",
            json=payload,
        )
        raise_for_response(response)

    async def get(self, link_id: str) -> IssueLink:
        response = await self._client.get(
            f"/rest/api/3/issueLink/{link_id}",
        )
        raise_for_response(response)
        return IssueLink.model_validate(response.json())

    async def delete(self, link_id: str) -> None:
        response = await self._client.delete(
            f"/rest/api/3/issueLink/{link_id}",
        )
        raise_for_response(response)

    async def get_link_types(self) -> list[IssueLinkType]:
        response = await self._client.get(
            "/rest/api/3/issueLinkType",
        )
        raise_for_response(response)
        data = response.json()
        return [
            IssueLinkType.model_validate(item)
            for item in data.get("issueLinkTypes", [])
        ]

    async def get_link_type(self, link_type_id: str) -> IssueLinkType:
        response = await self._client.get(
            f"/rest/api/3/issueLinkType/{link_type_id}",
        )
        raise_for_response(response)
        return IssueLinkType.model_validate(response.json())

    async def create_link_type(
        self,
        name: str,
        inward: str,
        outward: str,
    ) -> IssueLinkType:
        payload: dict[str, str] = {
            "name": name,
            "inward": inward,
            "outward": outward,
        }
        response = await self._client.post(
            "/rest/api/3/issueLinkType",
            json=payload,
        )
        raise_for_response(response)
        return IssueLinkType.model_validate(response.json())

    async def update_link_type(
        self,
        link_type_id: str,
        name: str,
        inward: str,
        outward: str,
    ) -> IssueLinkType:
        payload: dict[str, str] = {
            "name": name,
            "inward": inward,
            "outward": outward,
        }
        response = await self._client.put(
            f"/rest/api/3/issueLinkType/{link_type_id}",
            json=payload,
        )
        raise_for_response(response)
        return IssueLinkType.model_validate(response.json())

    async def delete_link_type(self, link_type_id: str) -> None:
        response = await self._client.delete(
            f"/rest/api/3/issueLinkType/{link_type_id}",
        )
        raise_for_response(response)
