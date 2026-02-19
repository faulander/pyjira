from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyjira.exceptions import raise_for_response
from pyjira.models.notification_scheme import (
    NotificationScheme,
    NotificationSchemePage,
)

if TYPE_CHECKING:
    import httpx


class NotificationSchemeResource:
    """Sync operations for Jira notification schemes."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def search(
        self,
        *,
        start_at: int = 0,
        max_results: int = 50,
        expand: list[str] | None = None,
    ) -> NotificationSchemePage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if expand:
            params["expand"] = ",".join(expand)
        response = self._client.get("/rest/api/3/notificationscheme", params=params)
        raise_for_response(response)
        return NotificationSchemePage.model_validate(response.json())

    def get(
        self,
        scheme_id: str,
        *,
        expand: list[str] | None = None,
    ) -> NotificationScheme:
        params: dict[str, str] = {}
        if expand:
            params["expand"] = ",".join(expand)
        response = self._client.get(
            f"/rest/api/3/notificationscheme/{scheme_id}",
            params=params,
        )
        raise_for_response(response)
        return NotificationScheme.model_validate(response.json())

    def create(self, body: dict[str, Any]) -> dict[str, Any]:
        response = self._client.post("/rest/api/3/notificationscheme", json=body)
        raise_for_response(response)
        return response.json()

    def update(self, scheme_id: str, body: dict[str, Any]) -> None:
        response = self._client.put(
            f"/rest/api/3/notificationscheme/{scheme_id}",
            json=body,
        )
        raise_for_response(response)

    def delete(self, scheme_id: str) -> None:
        response = self._client.delete(
            f"/rest/api/3/notificationscheme/{scheme_id}",
        )
        raise_for_response(response)

    def add_notifications(self, scheme_id: str, body: dict[str, Any]) -> None:
        response = self._client.put(
            f"/rest/api/3/notificationscheme/{scheme_id}/notification",
            json=body,
        )
        raise_for_response(response)

    def remove_notification(
        self,
        scheme_id: str,
        notification_id: str,
    ) -> None:
        response = self._client.delete(
            f"/rest/api/3/notificationscheme/{scheme_id}/notification/{notification_id}",
        )
        raise_for_response(response)


class AsyncNotificationSchemeResource:
    """Async operations for Jira notification schemes."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def search(
        self,
        *,
        start_at: int = 0,
        max_results: int = 50,
        expand: list[str] | None = None,
    ) -> NotificationSchemePage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if expand:
            params["expand"] = ",".join(expand)
        response = await self._client.get(
            "/rest/api/3/notificationscheme",
            params=params,
        )
        raise_for_response(response)
        return NotificationSchemePage.model_validate(response.json())

    async def get(
        self,
        scheme_id: str,
        *,
        expand: list[str] | None = None,
    ) -> NotificationScheme:
        params: dict[str, str] = {}
        if expand:
            params["expand"] = ",".join(expand)
        response = await self._client.get(
            f"/rest/api/3/notificationscheme/{scheme_id}",
            params=params,
        )
        raise_for_response(response)
        return NotificationScheme.model_validate(response.json())

    async def create(self, body: dict[str, Any]) -> dict[str, Any]:
        response = await self._client.post(
            "/rest/api/3/notificationscheme",
            json=body,
        )
        raise_for_response(response)
        return response.json()

    async def update(self, scheme_id: str, body: dict[str, Any]) -> None:
        response = await self._client.put(
            f"/rest/api/3/notificationscheme/{scheme_id}",
            json=body,
        )
        raise_for_response(response)

    async def delete(self, scheme_id: str) -> None:
        response = await self._client.delete(
            f"/rest/api/3/notificationscheme/{scheme_id}",
        )
        raise_for_response(response)

    async def add_notifications(self, scheme_id: str, body: dict[str, Any]) -> None:
        response = await self._client.put(
            f"/rest/api/3/notificationscheme/{scheme_id}/notification",
            json=body,
        )
        raise_for_response(response)

    async def remove_notification(
        self,
        scheme_id: str,
        notification_id: str,
    ) -> None:
        response = await self._client.delete(
            f"/rest/api/3/notificationscheme/{scheme_id}/notification/{notification_id}",
        )
        raise_for_response(response)
