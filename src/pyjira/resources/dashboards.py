from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyjira.exceptions import raise_for_response
from pyjira.models.dashboard import Dashboard, DashboardGadget, DashboardPage

if TYPE_CHECKING:
    import httpx


class DashboardResource:
    """Sync operations for Jira dashboards."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def list(
        self,
        *,
        start_at: int = 0,
        max_results: int = 50,
    ) -> DashboardPage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        response = self._client.get("/rest/api/3/dashboard", params=params)
        raise_for_response(response)
        return DashboardPage.model_validate(response.json())

    def search(
        self,
        *,
        filter_str: str | None = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> dict[str, Any]:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if filter_str:
            params["dashboardName"] = filter_str
        response = self._client.get(
            "/rest/api/3/dashboard/search",
            params=params,
        )
        raise_for_response(response)
        return response.json()

    def create(self, body: dict[str, Any]) -> Dashboard:
        response = self._client.post("/rest/api/3/dashboard", json=body)
        raise_for_response(response)
        return Dashboard.model_validate(response.json())

    def get(self, dashboard_id: str) -> Dashboard:
        response = self._client.get(
            f"/rest/api/3/dashboard/{dashboard_id}",
        )
        raise_for_response(response)
        return Dashboard.model_validate(response.json())

    def update(
        self,
        dashboard_id: str,
        body: dict[str, Any],
    ) -> Dashboard:
        response = self._client.put(
            f"/rest/api/3/dashboard/{dashboard_id}",
            json=body,
        )
        raise_for_response(response)
        return Dashboard.model_validate(response.json())

    def delete(self, dashboard_id: str) -> None:
        response = self._client.delete(
            f"/rest/api/3/dashboard/{dashboard_id}",
        )
        raise_for_response(response)

    def copy(
        self,
        dashboard_id: str,
        body: dict[str, Any],
    ) -> Dashboard:
        response = self._client.post(
            f"/rest/api/3/dashboard/{dashboard_id}/copy",
            json=body,
        )
        raise_for_response(response)
        return Dashboard.model_validate(response.json())

    def get_gadgets(
        self,
        dashboard_id: str,
    ) -> list[DashboardGadget]:
        response = self._client.get(
            f"/rest/api/3/dashboard/{dashboard_id}/gadget",
        )
        raise_for_response(response)
        data = response.json()
        return [DashboardGadget.model_validate(g) for g in data.get("gadgets", [])]

    def add_gadget(
        self,
        dashboard_id: str,
        body: dict[str, Any],
    ) -> DashboardGadget:
        response = self._client.post(
            f"/rest/api/3/dashboard/{dashboard_id}/gadget",
            json=body,
        )
        raise_for_response(response)
        return DashboardGadget.model_validate(response.json())

    def update_gadget(
        self,
        dashboard_id: str,
        gadget_id: str,
        body: dict[str, Any],
    ) -> DashboardGadget:
        response = self._client.put(
            f"/rest/api/3/dashboard/{dashboard_id}/gadget/{gadget_id}",
            json=body,
        )
        raise_for_response(response)
        return DashboardGadget.model_validate(response.json())

    def remove_gadget(
        self,
        dashboard_id: str,
        gadget_id: str,
    ) -> None:
        response = self._client.delete(
            f"/rest/api/3/dashboard/{dashboard_id}/gadget/{gadget_id}",
        )
        raise_for_response(response)


class AsyncDashboardResource:
    """Async operations for Jira dashboards."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def list(
        self,
        *,
        start_at: int = 0,
        max_results: int = 50,
    ) -> DashboardPage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        response = await self._client.get(
            "/rest/api/3/dashboard",
            params=params,
        )
        raise_for_response(response)
        return DashboardPage.model_validate(response.json())

    async def search(
        self,
        *,
        filter_str: str | None = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> dict[str, Any]:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if filter_str:
            params["dashboardName"] = filter_str
        response = await self._client.get(
            "/rest/api/3/dashboard/search",
            params=params,
        )
        raise_for_response(response)
        return response.json()

    async def create(self, body: dict[str, Any]) -> Dashboard:
        response = await self._client.post(
            "/rest/api/3/dashboard",
            json=body,
        )
        raise_for_response(response)
        return Dashboard.model_validate(response.json())

    async def get(self, dashboard_id: str) -> Dashboard:
        response = await self._client.get(
            f"/rest/api/3/dashboard/{dashboard_id}",
        )
        raise_for_response(response)
        return Dashboard.model_validate(response.json())

    async def update(
        self,
        dashboard_id: str,
        body: dict[str, Any],
    ) -> Dashboard:
        response = await self._client.put(
            f"/rest/api/3/dashboard/{dashboard_id}",
            json=body,
        )
        raise_for_response(response)
        return Dashboard.model_validate(response.json())

    async def delete(self, dashboard_id: str) -> None:
        response = await self._client.delete(
            f"/rest/api/3/dashboard/{dashboard_id}",
        )
        raise_for_response(response)

    async def copy(
        self,
        dashboard_id: str,
        body: dict[str, Any],
    ) -> Dashboard:
        response = await self._client.post(
            f"/rest/api/3/dashboard/{dashboard_id}/copy",
            json=body,
        )
        raise_for_response(response)
        return Dashboard.model_validate(response.json())

    async def get_gadgets(
        self,
        dashboard_id: str,
    ) -> list[DashboardGadget]:
        response = await self._client.get(
            f"/rest/api/3/dashboard/{dashboard_id}/gadget",
        )
        raise_for_response(response)
        data = response.json()
        return [DashboardGadget.model_validate(g) for g in data.get("gadgets", [])]

    async def add_gadget(
        self,
        dashboard_id: str,
        body: dict[str, Any],
    ) -> DashboardGadget:
        response = await self._client.post(
            f"/rest/api/3/dashboard/{dashboard_id}/gadget",
            json=body,
        )
        raise_for_response(response)
        return DashboardGadget.model_validate(response.json())

    async def update_gadget(
        self,
        dashboard_id: str,
        gadget_id: str,
        body: dict[str, Any],
    ) -> DashboardGadget:
        response = await self._client.put(
            f"/rest/api/3/dashboard/{dashboard_id}/gadget/{gadget_id}",
            json=body,
        )
        raise_for_response(response)
        return DashboardGadget.model_validate(response.json())

    async def remove_gadget(
        self,
        dashboard_id: str,
        gadget_id: str,
    ) -> None:
        response = await self._client.delete(
            f"/rest/api/3/dashboard/{dashboard_id}/gadget/{gadget_id}",
        )
        raise_for_response(response)
