from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyjira.exceptions import raise_for_response
from pyjira.models.screen import (
    Screen,
    ScreenField,
    ScreenPage,
    ScreenSchemePage,
    ScreenTab,
)

if TYPE_CHECKING:
    import httpx


class ScreenResource:
    """Sync operations for Jira screens, tabs, fields, and screen schemes."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def list(
        self,
        *,
        start_at: int = 0,
        max_results: int = 100,
    ) -> ScreenPage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        response = self._client.get("/rest/api/3/screens", params=params)
        raise_for_response(response)
        return ScreenPage.model_validate(response.json())

    def create(self, body: dict[str, Any]) -> Screen:
        response = self._client.post("/rest/api/3/screens", json=body)
        raise_for_response(response)
        return Screen.model_validate(response.json())

    def update_screen(self, screen_id: str, body: dict[str, Any]) -> Screen:
        response = self._client.put(
            f"/rest/api/3/screens/{screen_id}",
            json=body,
        )
        raise_for_response(response)
        return Screen.model_validate(response.json())

    def delete_screen(self, screen_id: str) -> None:
        response = self._client.delete(f"/rest/api/3/screens/{screen_id}")
        raise_for_response(response)

    def get_tabs(self, screen_id: str) -> list[ScreenTab]:
        response = self._client.get(f"/rest/api/3/screens/{screen_id}/tabs")
        raise_for_response(response)
        return [ScreenTab.model_validate(item) for item in response.json()]

    def create_tab(self, screen_id: str, name: str) -> ScreenTab:
        response = self._client.post(
            f"/rest/api/3/screens/{screen_id}/tabs",
            json={"name": name},
        )
        raise_for_response(response)
        return ScreenTab.model_validate(response.json())

    def update_tab(self, screen_id: str, tab_id: str, name: str) -> ScreenTab:
        response = self._client.put(
            f"/rest/api/3/screens/{screen_id}/tabs/{tab_id}",
            json={"name": name},
        )
        raise_for_response(response)
        return ScreenTab.model_validate(response.json())

    def delete_tab(self, screen_id: str, tab_id: str) -> None:
        response = self._client.delete(
            f"/rest/api/3/screens/{screen_id}/tabs/{tab_id}",
        )
        raise_for_response(response)

    def get_tab_fields(self, screen_id: str, tab_id: str) -> list[ScreenField]:
        response = self._client.get(
            f"/rest/api/3/screens/{screen_id}/tabs/{tab_id}/fields",
        )
        raise_for_response(response)
        return [ScreenField.model_validate(item) for item in response.json()]

    def add_tab_field(
        self,
        screen_id: str,
        tab_id: str,
        field_id: str,
    ) -> ScreenField:
        response = self._client.post(
            f"/rest/api/3/screens/{screen_id}/tabs/{tab_id}/fields",
            json={"fieldId": field_id},
        )
        raise_for_response(response)
        return ScreenField.model_validate(response.json())

    def remove_tab_field(
        self,
        screen_id: str,
        tab_id: str,
        field_id: str,
    ) -> None:
        response = self._client.delete(
            f"/rest/api/3/screens/{screen_id}/tabs/{tab_id}/fields/{field_id}",
        )
        raise_for_response(response)

    def get_available_fields(self, screen_id: str) -> list[ScreenField]:
        response = self._client.get(
            f"/rest/api/3/screens/{screen_id}/availableFields",
        )
        raise_for_response(response)
        return [ScreenField.model_validate(item) for item in response.json()]

    def get_screen_schemes(
        self,
        *,
        start_at: int = 0,
        max_results: int = 25,
    ) -> ScreenSchemePage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        response = self._client.get("/rest/api/3/screenscheme", params=params)
        raise_for_response(response)
        return ScreenSchemePage.model_validate(response.json())


class AsyncScreenResource:
    """Async operations for Jira screens, tabs, fields, and screen schemes."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def list(
        self,
        *,
        start_at: int = 0,
        max_results: int = 100,
    ) -> ScreenPage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        response = await self._client.get("/rest/api/3/screens", params=params)
        raise_for_response(response)
        return ScreenPage.model_validate(response.json())

    async def create(self, body: dict[str, Any]) -> Screen:
        response = await self._client.post("/rest/api/3/screens", json=body)
        raise_for_response(response)
        return Screen.model_validate(response.json())

    async def update_screen(self, screen_id: str, body: dict[str, Any]) -> Screen:
        response = await self._client.put(
            f"/rest/api/3/screens/{screen_id}",
            json=body,
        )
        raise_for_response(response)
        return Screen.model_validate(response.json())

    async def delete_screen(self, screen_id: str) -> None:
        response = await self._client.delete(f"/rest/api/3/screens/{screen_id}")
        raise_for_response(response)

    async def get_tabs(self, screen_id: str) -> list[ScreenTab]:
        response = await self._client.get(f"/rest/api/3/screens/{screen_id}/tabs")
        raise_for_response(response)
        return [ScreenTab.model_validate(item) for item in response.json()]

    async def create_tab(self, screen_id: str, name: str) -> ScreenTab:
        response = await self._client.post(
            f"/rest/api/3/screens/{screen_id}/tabs",
            json={"name": name},
        )
        raise_for_response(response)
        return ScreenTab.model_validate(response.json())

    async def update_tab(self, screen_id: str, tab_id: str, name: str) -> ScreenTab:
        response = await self._client.put(
            f"/rest/api/3/screens/{screen_id}/tabs/{tab_id}",
            json={"name": name},
        )
        raise_for_response(response)
        return ScreenTab.model_validate(response.json())

    async def delete_tab(self, screen_id: str, tab_id: str) -> None:
        response = await self._client.delete(
            f"/rest/api/3/screens/{screen_id}/tabs/{tab_id}",
        )
        raise_for_response(response)

    async def get_tab_fields(self, screen_id: str, tab_id: str) -> list[ScreenField]:
        response = await self._client.get(
            f"/rest/api/3/screens/{screen_id}/tabs/{tab_id}/fields",
        )
        raise_for_response(response)
        return [ScreenField.model_validate(item) for item in response.json()]

    async def add_tab_field(
        self,
        screen_id: str,
        tab_id: str,
        field_id: str,
    ) -> ScreenField:
        response = await self._client.post(
            f"/rest/api/3/screens/{screen_id}/tabs/{tab_id}/fields",
            json={"fieldId": field_id},
        )
        raise_for_response(response)
        return ScreenField.model_validate(response.json())

    async def remove_tab_field(
        self,
        screen_id: str,
        tab_id: str,
        field_id: str,
    ) -> None:
        response = await self._client.delete(
            f"/rest/api/3/screens/{screen_id}/tabs/{tab_id}/fields/{field_id}",
        )
        raise_for_response(response)

    async def get_available_fields(self, screen_id: str) -> list[ScreenField]:
        response = await self._client.get(
            f"/rest/api/3/screens/{screen_id}/availableFields",
        )
        raise_for_response(response)
        return [ScreenField.model_validate(item) for item in response.json()]

    async def get_screen_schemes(
        self,
        *,
        start_at: int = 0,
        max_results: int = 25,
    ) -> ScreenSchemePage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        response = await self._client.get("/rest/api/3/screenscheme", params=params)
        raise_for_response(response)
        return ScreenSchemePage.model_validate(response.json())
