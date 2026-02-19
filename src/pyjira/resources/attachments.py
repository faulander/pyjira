from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyjira.exceptions import raise_for_response

if TYPE_CHECKING:
    import httpx


class AttachmentResource:
    """Sync operations for Jira attachments."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def get_meta(self) -> dict[str, Any]:
        response = self._client.get("/rest/api/3/attachment/meta")
        raise_for_response(response)
        return response.json()

    def get(self, attachment_id: str) -> dict[str, Any]:
        response = self._client.get(
            f"/rest/api/3/attachment/{attachment_id}",
        )
        raise_for_response(response)
        return response.json()

    def delete(self, attachment_id: str) -> None:
        response = self._client.delete(
            f"/rest/api/3/attachment/{attachment_id}",
        )
        raise_for_response(response)

    def get_content(self, attachment_id: str) -> bytes:
        response = self._client.get(
            f"/rest/api/3/attachment/content/{attachment_id}",
        )
        raise_for_response(response)
        return response.content

    def get_thumbnail(self, attachment_id: str) -> bytes:
        response = self._client.get(
            f"/rest/api/3/attachment/thumbnail/{attachment_id}",
        )
        raise_for_response(response)
        return response.content

    def expand_human(self, attachment_id: str) -> dict[str, Any]:
        response = self._client.get(
            f"/rest/api/3/attachment/{attachment_id}/expand/human",
        )
        raise_for_response(response)
        return response.json()

    def expand_raw(self, attachment_id: str) -> dict[str, Any]:
        response = self._client.get(
            f"/rest/api/3/attachment/{attachment_id}/expand/raw",
        )
        raise_for_response(response)
        return response.json()


class AsyncAttachmentResource:
    """Async operations for Jira attachments."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def get_meta(self) -> dict[str, Any]:
        response = await self._client.get("/rest/api/3/attachment/meta")
        raise_for_response(response)
        return response.json()

    async def get(self, attachment_id: str) -> dict[str, Any]:
        response = await self._client.get(
            f"/rest/api/3/attachment/{attachment_id}",
        )
        raise_for_response(response)
        return response.json()

    async def delete(self, attachment_id: str) -> None:
        response = await self._client.delete(
            f"/rest/api/3/attachment/{attachment_id}",
        )
        raise_for_response(response)

    async def get_content(self, attachment_id: str) -> bytes:
        response = await self._client.get(
            f"/rest/api/3/attachment/content/{attachment_id}",
        )
        raise_for_response(response)
        return response.content

    async def get_thumbnail(self, attachment_id: str) -> bytes:
        response = await self._client.get(
            f"/rest/api/3/attachment/thumbnail/{attachment_id}",
        )
        raise_for_response(response)
        return response.content

    async def expand_human(self, attachment_id: str) -> dict[str, Any]:
        response = await self._client.get(
            f"/rest/api/3/attachment/{attachment_id}/expand/human",
        )
        raise_for_response(response)
        return response.json()

    async def expand_raw(self, attachment_id: str) -> dict[str, Any]:
        response = await self._client.get(
            f"/rest/api/3/attachment/{attachment_id}/expand/raw",
        )
        raise_for_response(response)
        return response.json()
