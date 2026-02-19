from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyjira.exceptions import raise_for_response

if TYPE_CHECKING:
    import httpx


class ServerInfoResource:
    """Sync operations for Jira server information and configuration."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def get(self) -> dict[str, Any]:
        response = self._client.get("/rest/api/3/serverInfo")
        raise_for_response(response)
        return response.json()

    def get_configuration(self) -> dict[str, Any]:
        response = self._client.get("/rest/api/3/configuration")
        raise_for_response(response)
        return response.json()


class AsyncServerInfoResource:
    """Async operations for Jira server information and configuration."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def get(self) -> dict[str, Any]:
        response = await self._client.get("/rest/api/3/serverInfo")
        raise_for_response(response)
        return response.json()

    async def get_configuration(self) -> dict[str, Any]:
        response = await self._client.get("/rest/api/3/configuration")
        raise_for_response(response)
        return response.json()
