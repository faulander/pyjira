from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyjira.exceptions import raise_for_response
from pyjira.models.workflow import Workflow, WorkflowPage, WorkflowScheme

if TYPE_CHECKING:
    import httpx


class WorkflowResource:
    """Sync operations for Jira workflows and workflow schemes."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def list(
        self,
        *,
        workflow_name: str | None = None,
        expand: list[str] | None = None,
    ) -> list[Workflow]:
        params: dict[str, str] = {}
        if workflow_name:
            params["workflowName"] = workflow_name
        if expand:
            params["expand"] = ",".join(expand)
        response = self._client.get("/rest/api/3/workflow", params=params)
        raise_for_response(response)
        return [Workflow.model_validate(item) for item in response.json()]

    def search(
        self,
        *,
        start_at: int = 0,
        max_results: int = 50,
        expand: list[str] | None = None,
        query_string: str | None = None,
    ) -> WorkflowPage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if expand:
            params["expand"] = ",".join(expand)
        if query_string:
            params["queryString"] = query_string
        response = self._client.get("/rest/api/3/workflow/search", params=params)
        raise_for_response(response)
        return WorkflowPage.model_validate(response.json())

    def create(self, body: dict[str, Any]) -> Workflow:
        response = self._client.post("/rest/api/3/workflow", json=body)
        raise_for_response(response)
        return Workflow.model_validate(response.json())

    def delete(self, workflow_id: str) -> None:
        response = self._client.delete(f"/rest/api/3/workflow/{workflow_id}")
        raise_for_response(response)

    def get_all_schemes(
        self,
        *,
        start_at: int = 0,
        max_results: int = 50,
    ) -> dict[str, Any]:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        response = self._client.get("/rest/api/3/workflowscheme", params=params)
        raise_for_response(response)
        return response.json()

    def get_scheme(self, scheme_id: str) -> WorkflowScheme:
        response = self._client.get(f"/rest/api/3/workflowscheme/{scheme_id}")
        raise_for_response(response)
        return WorkflowScheme.model_validate(response.json())

    def create_scheme(self, body: dict[str, Any]) -> WorkflowScheme:
        response = self._client.post("/rest/api/3/workflowscheme", json=body)
        raise_for_response(response)
        return WorkflowScheme.model_validate(response.json())

    def update_scheme(self, scheme_id: str, body: dict[str, Any]) -> WorkflowScheme:
        response = self._client.put(
            f"/rest/api/3/workflowscheme/{scheme_id}",
            json=body,
        )
        raise_for_response(response)
        return WorkflowScheme.model_validate(response.json())

    def delete_scheme(self, scheme_id: str) -> None:
        response = self._client.delete(f"/rest/api/3/workflowscheme/{scheme_id}")
        raise_for_response(response)


class AsyncWorkflowResource:
    """Async operations for Jira workflows and workflow schemes."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def list(
        self,
        *,
        workflow_name: str | None = None,
        expand: list[str] | None = None,
    ) -> list[Workflow]:
        params: dict[str, str] = {}
        if workflow_name:
            params["workflowName"] = workflow_name
        if expand:
            params["expand"] = ",".join(expand)
        response = await self._client.get("/rest/api/3/workflow", params=params)
        raise_for_response(response)
        return [Workflow.model_validate(item) for item in response.json()]

    async def search(
        self,
        *,
        start_at: int = 0,
        max_results: int = 50,
        expand: list[str] | None = None,
        query_string: str | None = None,
    ) -> WorkflowPage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if expand:
            params["expand"] = ",".join(expand)
        if query_string:
            params["queryString"] = query_string
        response = await self._client.get("/rest/api/3/workflow/search", params=params)
        raise_for_response(response)
        return WorkflowPage.model_validate(response.json())

    async def create(self, body: dict[str, Any]) -> Workflow:
        response = await self._client.post("/rest/api/3/workflow", json=body)
        raise_for_response(response)
        return Workflow.model_validate(response.json())

    async def delete(self, workflow_id: str) -> None:
        response = await self._client.delete(f"/rest/api/3/workflow/{workflow_id}")
        raise_for_response(response)

    async def get_all_schemes(
        self,
        *,
        start_at: int = 0,
        max_results: int = 50,
    ) -> dict[str, Any]:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        response = await self._client.get("/rest/api/3/workflowscheme", params=params)
        raise_for_response(response)
        return response.json()

    async def get_scheme(self, scheme_id: str) -> WorkflowScheme:
        response = await self._client.get(f"/rest/api/3/workflowscheme/{scheme_id}")
        raise_for_response(response)
        return WorkflowScheme.model_validate(response.json())

    async def create_scheme(self, body: dict[str, Any]) -> WorkflowScheme:
        response = await self._client.post("/rest/api/3/workflowscheme", json=body)
        raise_for_response(response)
        return WorkflowScheme.model_validate(response.json())

    async def update_scheme(
        self, scheme_id: str, body: dict[str, Any]
    ) -> WorkflowScheme:
        response = await self._client.put(
            f"/rest/api/3/workflowscheme/{scheme_id}",
            json=body,
        )
        raise_for_response(response)
        return WorkflowScheme.model_validate(response.json())

    async def delete_scheme(self, scheme_id: str) -> None:
        response = await self._client.delete(f"/rest/api/3/workflowscheme/{scheme_id}")
        raise_for_response(response)
