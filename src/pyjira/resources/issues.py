from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from pyjira.exceptions import raise_for_response
from pyjira.models.issue import (
    Attachment,
    ChangeHistory,
    ChangelogPage,
    Issue,
    PropertyKey,
    RemoteIssueLink,
    Transition,
    Votes,
    Watchers,
    Worklog,
    WorklogPage,
)

if TYPE_CHECKING:
    import httpx


def _build_params(
    *,
    fields: list[str] | None = None,
    expand: list[str] | None = None,
    properties: list[str] | None = None,
) -> dict[str, str]:
    params: dict[str, str] = {}
    if fields:
        params["fields"] = ",".join(fields)
    if expand:
        params["expand"] = ",".join(expand)
    if properties:
        params["properties"] = ",".join(properties)
    return params


class IssueResource:
    """Sync operations for Jira issues."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    # ── Core CRUD ──────────────────────────────────────────────────────

    def get(
        self,
        issue_id_or_key: str,
        *,
        fields: list[str] | None = None,
        expand: list[str] | None = None,
        properties: list[str] | None = None,
    ) -> Issue:
        params = _build_params(fields=fields, expand=expand, properties=properties)
        response = self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}", params=params
        )
        raise_for_response(response)
        return Issue.model_validate(response.json())

    def create(
        self,
        fields: dict[str, Any],
        *,
        update: dict[str, Any] | None = None,
    ) -> Issue:
        body: dict[str, Any] = {"fields": fields}
        if update:
            body["update"] = update
        response = self._client.post("/rest/api/3/issue", json=body)
        raise_for_response(response)
        return Issue.model_validate(response.json())

    def update(
        self,
        issue_id_or_key: str,
        *,
        fields: dict[str, Any] | None = None,
        update: dict[str, Any] | None = None,
        notify_users: bool = True,
    ) -> None:
        body: dict[str, Any] = {}
        if fields:
            body["fields"] = fields
        if update:
            body["update"] = update
        params = {} if notify_users else {"notifyUsers": "false"}
        response = self._client.put(
            f"/rest/api/3/issue/{issue_id_or_key}",
            json=body,
            params=params,
        )
        raise_for_response(response)

    def delete(
        self,
        issue_id_or_key: str,
        *,
        delete_subtasks: bool = False,
    ) -> None:
        params = {"deleteSubtasks": str(delete_subtasks).lower()}
        response = self._client.delete(
            f"/rest/api/3/issue/{issue_id_or_key}",
            params=params,
        )
        raise_for_response(response)

    # ── Assign ─────────────────────────────────────────────────────────

    def assign(
        self,
        issue_id_or_key: str,
        *,
        account_id: str | None = None,
    ) -> None:
        body: dict[str, Any] = {"accountId": account_id}
        response = self._client.put(
            f"/rest/api/3/issue/{issue_id_or_key}/assignee",
            json=body,
        )
        raise_for_response(response)

    # ── Attachments ────────────────────────────────────────────────────

    def add_attachment(
        self,
        issue_id_or_key: str,
        *,
        file_path: str | Path | None = None,
        filename: str | None = None,
        content: bytes | None = None,
    ) -> list[Attachment]:
        if file_path:
            path = Path(file_path)
            file_tuple = (path.name, path.read_bytes())
        elif filename and content is not None:
            file_tuple = (filename, content)
        else:
            raise ValueError("Provide either file_path or both filename and content")
        response = self._client.post(
            f"/rest/api/3/issue/{issue_id_or_key}/attachments",
            files={"file": file_tuple},
            headers={"X-Atlassian-Token": "no-check"},
            content=None,
        )
        raise_for_response(response)
        return [Attachment.model_validate(a) for a in response.json()]

    # ── Changelogs ─────────────────────────────────────────────────────

    def get_changelogs(
        self,
        issue_id_or_key: str,
        *,
        start_at: int = 0,
        max_results: int = 100,
    ) -> ChangelogPage:
        params = {"startAt": str(start_at), "maxResults": str(max_results)}
        response = self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/changelog",
            params=params,
        )
        raise_for_response(response)
        return ChangelogPage.model_validate(response.json())

    def get_changelogs_by_ids(
        self,
        issue_id_or_key: str,
        changelog_ids: list[int],
    ) -> list[ChangeHistory]:
        response = self._client.post(
            f"/rest/api/3/issue/{issue_id_or_key}/changelog/list",
            json={"changelogIds": changelog_ids},
        )
        raise_for_response(response)
        data = response.json()
        return [ChangeHistory.model_validate(h) for h in data.get("values", [])]

    # ── Edit metadata ──────────────────────────────────────────────────

    def get_edit_meta(
        self,
        issue_id_or_key: str,
        *,
        override_screen_security: bool = False,
        override_editable_flag: bool = False,
    ) -> dict[str, Any]:
        params: dict[str, str] = {}
        if override_screen_security:
            params["overrideScreenSecurity"] = "true"
        if override_editable_flag:
            params["overrideEditableFlag"] = "true"
        response = self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/editmeta",
            params=params,
        )
        raise_for_response(response)
        return response.json()

    # ── Notify ─────────────────────────────────────────────────────────

    def notify(
        self,
        issue_id_or_key: str,
        body: dict[str, Any],
    ) -> None:
        response = self._client.post(
            f"/rest/api/3/issue/{issue_id_or_key}/notify",
            json=body,
        )
        raise_for_response(response)

    # ── Properties ─────────────────────────────────────────────────────

    def get_property_keys(
        self,
        issue_id_or_key: str,
    ) -> list[PropertyKey]:
        response = self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/properties",
        )
        raise_for_response(response)
        data = response.json()
        return [PropertyKey.model_validate(k) for k in data.get("keys", [])]

    def get_property(
        self,
        issue_id_or_key: str,
        property_key: str,
    ) -> dict[str, Any]:
        response = self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/properties/{property_key}",
        )
        raise_for_response(response)
        return response.json()

    def set_property(
        self,
        issue_id_or_key: str,
        property_key: str,
        value: Any,
    ) -> None:
        response = self._client.put(
            f"/rest/api/3/issue/{issue_id_or_key}/properties/{property_key}",
            json=value,
        )
        raise_for_response(response)

    def delete_property(
        self,
        issue_id_or_key: str,
        property_key: str,
    ) -> None:
        response = self._client.delete(
            f"/rest/api/3/issue/{issue_id_or_key}/properties/{property_key}",
        )
        raise_for_response(response)

    # ── Remote links ───────────────────────────────────────────────────

    def get_remote_links(
        self,
        issue_id_or_key: str,
        *,
        global_id: str | None = None,
    ) -> list[RemoteIssueLink]:
        params: dict[str, str] = {}
        if global_id:
            params["globalId"] = global_id
        response = self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/remotelink",
            params=params,
        )
        raise_for_response(response)
        return [RemoteIssueLink.model_validate(r) for r in response.json()]

    def create_or_update_remote_link(
        self,
        issue_id_or_key: str,
        body: dict[str, Any],
    ) -> dict[str, Any]:
        response = self._client.post(
            f"/rest/api/3/issue/{issue_id_or_key}/remotelink",
            json=body,
        )
        raise_for_response(response)
        return response.json()

    def get_remote_link(
        self,
        issue_id_or_key: str,
        link_id: str,
    ) -> RemoteIssueLink:
        response = self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/remotelink/{link_id}",
        )
        raise_for_response(response)
        return RemoteIssueLink.model_validate(response.json())

    def update_remote_link(
        self,
        issue_id_or_key: str,
        link_id: str,
        body: dict[str, Any],
    ) -> None:
        response = self._client.put(
            f"/rest/api/3/issue/{issue_id_or_key}/remotelink/{link_id}",
            json=body,
        )
        raise_for_response(response)

    def delete_remote_link_by_global_id(
        self,
        issue_id_or_key: str,
        global_id: str,
    ) -> None:
        response = self._client.delete(
            f"/rest/api/3/issue/{issue_id_or_key}/remotelink",
            params={"globalId": global_id},
        )
        raise_for_response(response)

    def delete_remote_link(
        self,
        issue_id_or_key: str,
        link_id: str,
    ) -> None:
        response = self._client.delete(
            f"/rest/api/3/issue/{issue_id_or_key}/remotelink/{link_id}",
        )
        raise_for_response(response)

    # ── Transitions ────────────────────────────────────────────────────

    def get_transitions(
        self,
        issue_id_or_key: str,
        *,
        expand: list[str] | None = None,
    ) -> list[Transition]:
        params: dict[str, str] = {}
        if expand:
            params["expand"] = ",".join(expand)
        response = self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/transitions",
            params=params,
        )
        raise_for_response(response)
        data = response.json()
        return [Transition.model_validate(t) for t in data.get("transitions", [])]

    def transition(
        self,
        issue_id_or_key: str,
        transition_id: str,
        *,
        fields: dict[str, Any] | None = None,
        update: dict[str, Any] | None = None,
        comment: dict[str, Any] | None = None,
    ) -> None:
        body: dict[str, Any] = {"transition": {"id": transition_id}}
        if fields:
            body["fields"] = fields
        if update:
            body["update"] = update
        if comment:
            body["update"] = body.get("update", {})
            body["update"]["comment"] = [{"add": {"body": comment}}]
        response = self._client.post(
            f"/rest/api/3/issue/{issue_id_or_key}/transitions",
            json=body,
        )
        raise_for_response(response)

    # ── Votes ──────────────────────────────────────────────────────────

    def get_votes(self, issue_id_or_key: str) -> Votes:
        response = self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/votes",
        )
        raise_for_response(response)
        return Votes.model_validate(response.json())

    def add_vote(self, issue_id_or_key: str) -> None:
        response = self._client.post(
            f"/rest/api/3/issue/{issue_id_or_key}/votes",
        )
        raise_for_response(response)

    def remove_vote(self, issue_id_or_key: str) -> None:
        response = self._client.delete(
            f"/rest/api/3/issue/{issue_id_or_key}/votes",
        )
        raise_for_response(response)

    # ── Watchers ───────────────────────────────────────────────────────

    def get_watchers(self, issue_id_or_key: str) -> Watchers:
        response = self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/watchers",
        )
        raise_for_response(response)
        return Watchers.model_validate(response.json())

    def add_watcher(
        self,
        issue_id_or_key: str,
        account_id: str,
    ) -> None:
        response = self._client.post(
            f"/rest/api/3/issue/{issue_id_or_key}/watchers",
            json=account_id,
        )
        raise_for_response(response)

    def remove_watcher(
        self,
        issue_id_or_key: str,
        *,
        account_id: str | None = None,
    ) -> None:
        params: dict[str, str] = {}
        if account_id:
            params["accountId"] = account_id
        response = self._client.delete(
            f"/rest/api/3/issue/{issue_id_or_key}/watchers",
            params=params,
        )
        raise_for_response(response)

    # ── Worklogs ───────────────────────────────────────────────────────

    def get_worklogs(
        self,
        issue_id_or_key: str,
        *,
        start_at: int = 0,
        max_results: int = 5000,
        started_after: int | None = None,
        started_before: int | None = None,
        expand: list[str] | None = None,
    ) -> WorklogPage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if started_after is not None:
            params["startedAfter"] = str(started_after)
        if started_before is not None:
            params["startedBefore"] = str(started_before)
        if expand:
            params["expand"] = ",".join(expand)
        response = self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/worklog",
            params=params,
        )
        raise_for_response(response)
        return WorklogPage.model_validate(response.json())

    def add_worklog(
        self,
        issue_id_or_key: str,
        body: dict[str, Any],
        *,
        notify_users: bool = True,
        adjust_estimate: str | None = None,
        new_estimate: str | None = None,
        reduce_by: str | None = None,
        expand: list[str] | None = None,
        override_editable_flag: bool = False,
    ) -> Worklog:
        params: dict[str, str] = {}
        if not notify_users:
            params["notifyUsers"] = "false"
        if adjust_estimate:
            params["adjustEstimate"] = adjust_estimate
        if new_estimate:
            params["newEstimate"] = new_estimate
        if reduce_by:
            params["reduceBy"] = reduce_by
        if expand:
            params["expand"] = ",".join(expand)
        if override_editable_flag:
            params["overrideEditableFlag"] = "true"
        response = self._client.post(
            f"/rest/api/3/issue/{issue_id_or_key}/worklog",
            json=body,
            params=params,
        )
        raise_for_response(response)
        return Worklog.model_validate(response.json())

    def get_worklog(
        self,
        issue_id_or_key: str,
        worklog_id: str,
        *,
        expand: list[str] | None = None,
    ) -> Worklog:
        params: dict[str, str] = {}
        if expand:
            params["expand"] = ",".join(expand)
        response = self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/worklog/{worklog_id}",
            params=params,
        )
        raise_for_response(response)
        return Worklog.model_validate(response.json())

    def update_worklog(
        self,
        issue_id_or_key: str,
        worklog_id: str,
        body: dict[str, Any],
        *,
        notify_users: bool = True,
        adjust_estimate: str | None = None,
        new_estimate: str | None = None,
        expand: list[str] | None = None,
        override_editable_flag: bool = False,
    ) -> Worklog:
        params: dict[str, str] = {}
        if not notify_users:
            params["notifyUsers"] = "false"
        if adjust_estimate:
            params["adjustEstimate"] = adjust_estimate
        if new_estimate:
            params["newEstimate"] = new_estimate
        if expand:
            params["expand"] = ",".join(expand)
        if override_editable_flag:
            params["overrideEditableFlag"] = "true"
        response = self._client.put(
            f"/rest/api/3/issue/{issue_id_or_key}/worklog/{worklog_id}",
            json=body,
            params=params,
        )
        raise_for_response(response)
        return Worklog.model_validate(response.json())

    def delete_worklog(
        self,
        issue_id_or_key: str,
        worklog_id: str,
        *,
        notify_users: bool = True,
        adjust_estimate: str | None = None,
        new_estimate: str | None = None,
        increase_by: str | None = None,
        override_editable_flag: bool = False,
    ) -> None:
        params: dict[str, str] = {}
        if not notify_users:
            params["notifyUsers"] = "false"
        if adjust_estimate:
            params["adjustEstimate"] = adjust_estimate
        if new_estimate:
            params["newEstimate"] = new_estimate
        if increase_by:
            params["increaseBy"] = increase_by
        if override_editable_flag:
            params["overrideEditableFlag"] = "true"
        response = self._client.delete(
            f"/rest/api/3/issue/{issue_id_or_key}/worklog/{worklog_id}",
            params=params,
        )
        raise_for_response(response)


class AsyncIssueResource:
    """Async operations for Jira issues."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    # ── Core CRUD ──────────────────────────────────────────────────────

    async def get(
        self,
        issue_id_or_key: str,
        *,
        fields: list[str] | None = None,
        expand: list[str] | None = None,
        properties: list[str] | None = None,
    ) -> Issue:
        params = _build_params(fields=fields, expand=expand, properties=properties)
        response = await self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}", params=params
        )
        raise_for_response(response)
        return Issue.model_validate(response.json())

    async def create(
        self,
        fields: dict[str, Any],
        *,
        update: dict[str, Any] | None = None,
    ) -> Issue:
        body: dict[str, Any] = {"fields": fields}
        if update:
            body["update"] = update
        response = await self._client.post("/rest/api/3/issue", json=body)
        raise_for_response(response)
        return Issue.model_validate(response.json())

    async def update(
        self,
        issue_id_or_key: str,
        *,
        fields: dict[str, Any] | None = None,
        update: dict[str, Any] | None = None,
        notify_users: bool = True,
    ) -> None:
        body: dict[str, Any] = {}
        if fields:
            body["fields"] = fields
        if update:
            body["update"] = update
        params = {} if notify_users else {"notifyUsers": "false"}
        response = await self._client.put(
            f"/rest/api/3/issue/{issue_id_or_key}",
            json=body,
            params=params,
        )
        raise_for_response(response)

    async def delete(
        self,
        issue_id_or_key: str,
        *,
        delete_subtasks: bool = False,
    ) -> None:
        params = {"deleteSubtasks": str(delete_subtasks).lower()}
        response = await self._client.delete(
            f"/rest/api/3/issue/{issue_id_or_key}",
            params=params,
        )
        raise_for_response(response)

    # ── Assign ─────────────────────────────────────────────────────────

    async def assign(
        self,
        issue_id_or_key: str,
        *,
        account_id: str | None = None,
    ) -> None:
        body: dict[str, Any] = {"accountId": account_id}
        response = await self._client.put(
            f"/rest/api/3/issue/{issue_id_or_key}/assignee",
            json=body,
        )
        raise_for_response(response)

    # ── Attachments ────────────────────────────────────────────────────

    async def add_attachment(
        self,
        issue_id_or_key: str,
        *,
        file_path: str | Path | None = None,
        filename: str | None = None,
        content: bytes | None = None,
    ) -> list[Attachment]:
        if file_path:
            path = Path(file_path)
            file_tuple = (path.name, path.read_bytes())
        elif filename and content is not None:
            file_tuple = (filename, content)
        else:
            raise ValueError("Provide either file_path or both filename and content")
        response = await self._client.post(
            f"/rest/api/3/issue/{issue_id_or_key}/attachments",
            files={"file": file_tuple},
            headers={"X-Atlassian-Token": "no-check"},
            content=None,
        )
        raise_for_response(response)
        return [Attachment.model_validate(a) for a in response.json()]

    # ── Changelogs ─────────────────────────────────────────────────────

    async def get_changelogs(
        self,
        issue_id_or_key: str,
        *,
        start_at: int = 0,
        max_results: int = 100,
    ) -> ChangelogPage:
        params = {"startAt": str(start_at), "maxResults": str(max_results)}
        response = await self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/changelog",
            params=params,
        )
        raise_for_response(response)
        return ChangelogPage.model_validate(response.json())

    async def get_changelogs_by_ids(
        self,
        issue_id_or_key: str,
        changelog_ids: list[int],
    ) -> list[ChangeHistory]:
        response = await self._client.post(
            f"/rest/api/3/issue/{issue_id_or_key}/changelog/list",
            json={"changelogIds": changelog_ids},
        )
        raise_for_response(response)
        data = response.json()
        return [ChangeHistory.model_validate(h) for h in data.get("values", [])]

    # ── Edit metadata ──────────────────────────────────────────────────

    async def get_edit_meta(
        self,
        issue_id_or_key: str,
        *,
        override_screen_security: bool = False,
        override_editable_flag: bool = False,
    ) -> dict[str, Any]:
        params: dict[str, str] = {}
        if override_screen_security:
            params["overrideScreenSecurity"] = "true"
        if override_editable_flag:
            params["overrideEditableFlag"] = "true"
        response = await self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/editmeta",
            params=params,
        )
        raise_for_response(response)
        return response.json()

    # ── Notify ─────────────────────────────────────────────────────────

    async def notify(
        self,
        issue_id_or_key: str,
        body: dict[str, Any],
    ) -> None:
        response = await self._client.post(
            f"/rest/api/3/issue/{issue_id_or_key}/notify",
            json=body,
        )
        raise_for_response(response)

    # ── Properties ─────────────────────────────────────────────────────

    async def get_property_keys(
        self,
        issue_id_or_key: str,
    ) -> list[PropertyKey]:
        response = await self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/properties",
        )
        raise_for_response(response)
        data = response.json()
        return [PropertyKey.model_validate(k) for k in data.get("keys", [])]

    async def get_property(
        self,
        issue_id_or_key: str,
        property_key: str,
    ) -> dict[str, Any]:
        response = await self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/properties/{property_key}",
        )
        raise_for_response(response)
        return response.json()

    async def set_property(
        self,
        issue_id_or_key: str,
        property_key: str,
        value: Any,
    ) -> None:
        response = await self._client.put(
            f"/rest/api/3/issue/{issue_id_or_key}/properties/{property_key}",
            json=value,
        )
        raise_for_response(response)

    async def delete_property(
        self,
        issue_id_or_key: str,
        property_key: str,
    ) -> None:
        response = await self._client.delete(
            f"/rest/api/3/issue/{issue_id_or_key}/properties/{property_key}",
        )
        raise_for_response(response)

    # ── Remote links ───────────────────────────────────────────────────

    async def get_remote_links(
        self,
        issue_id_or_key: str,
        *,
        global_id: str | None = None,
    ) -> list[RemoteIssueLink]:
        params: dict[str, str] = {}
        if global_id:
            params["globalId"] = global_id
        response = await self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/remotelink",
            params=params,
        )
        raise_for_response(response)
        return [RemoteIssueLink.model_validate(r) for r in response.json()]

    async def create_or_update_remote_link(
        self,
        issue_id_or_key: str,
        body: dict[str, Any],
    ) -> dict[str, Any]:
        response = await self._client.post(
            f"/rest/api/3/issue/{issue_id_or_key}/remotelink",
            json=body,
        )
        raise_for_response(response)
        return response.json()

    async def get_remote_link(
        self,
        issue_id_or_key: str,
        link_id: str,
    ) -> RemoteIssueLink:
        response = await self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/remotelink/{link_id}",
        )
        raise_for_response(response)
        return RemoteIssueLink.model_validate(response.json())

    async def update_remote_link(
        self,
        issue_id_or_key: str,
        link_id: str,
        body: dict[str, Any],
    ) -> None:
        response = await self._client.put(
            f"/rest/api/3/issue/{issue_id_or_key}/remotelink/{link_id}",
            json=body,
        )
        raise_for_response(response)

    async def delete_remote_link_by_global_id(
        self,
        issue_id_or_key: str,
        global_id: str,
    ) -> None:
        response = await self._client.delete(
            f"/rest/api/3/issue/{issue_id_or_key}/remotelink",
            params={"globalId": global_id},
        )
        raise_for_response(response)

    async def delete_remote_link(
        self,
        issue_id_or_key: str,
        link_id: str,
    ) -> None:
        response = await self._client.delete(
            f"/rest/api/3/issue/{issue_id_or_key}/remotelink/{link_id}",
        )
        raise_for_response(response)

    # ── Transitions ────────────────────────────────────────────────────

    async def get_transitions(
        self,
        issue_id_or_key: str,
        *,
        expand: list[str] | None = None,
    ) -> list[Transition]:
        params: dict[str, str] = {}
        if expand:
            params["expand"] = ",".join(expand)
        response = await self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/transitions",
            params=params,
        )
        raise_for_response(response)
        data = response.json()
        return [Transition.model_validate(t) for t in data.get("transitions", [])]

    async def transition(
        self,
        issue_id_or_key: str,
        transition_id: str,
        *,
        fields: dict[str, Any] | None = None,
        update: dict[str, Any] | None = None,
        comment: dict[str, Any] | None = None,
    ) -> None:
        body: dict[str, Any] = {"transition": {"id": transition_id}}
        if fields:
            body["fields"] = fields
        if update:
            body["update"] = update
        if comment:
            body["update"] = body.get("update", {})
            body["update"]["comment"] = [{"add": {"body": comment}}]
        response = await self._client.post(
            f"/rest/api/3/issue/{issue_id_or_key}/transitions",
            json=body,
        )
        raise_for_response(response)

    # ── Votes ──────────────────────────────────────────────────────────

    async def get_votes(self, issue_id_or_key: str) -> Votes:
        response = await self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/votes",
        )
        raise_for_response(response)
        return Votes.model_validate(response.json())

    async def add_vote(self, issue_id_or_key: str) -> None:
        response = await self._client.post(
            f"/rest/api/3/issue/{issue_id_or_key}/votes",
        )
        raise_for_response(response)

    async def remove_vote(self, issue_id_or_key: str) -> None:
        response = await self._client.delete(
            f"/rest/api/3/issue/{issue_id_or_key}/votes",
        )
        raise_for_response(response)

    # ── Watchers ───────────────────────────────────────────────────────

    async def get_watchers(self, issue_id_or_key: str) -> Watchers:
        response = await self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/watchers",
        )
        raise_for_response(response)
        return Watchers.model_validate(response.json())

    async def add_watcher(
        self,
        issue_id_or_key: str,
        account_id: str,
    ) -> None:
        response = await self._client.post(
            f"/rest/api/3/issue/{issue_id_or_key}/watchers",
            json=account_id,
        )
        raise_for_response(response)

    async def remove_watcher(
        self,
        issue_id_or_key: str,
        *,
        account_id: str | None = None,
    ) -> None:
        params: dict[str, str] = {}
        if account_id:
            params["accountId"] = account_id
        response = await self._client.delete(
            f"/rest/api/3/issue/{issue_id_or_key}/watchers",
            params=params,
        )
        raise_for_response(response)

    # ── Worklogs ───────────────────────────────────────────────────────

    async def get_worklogs(
        self,
        issue_id_or_key: str,
        *,
        start_at: int = 0,
        max_results: int = 5000,
        started_after: int | None = None,
        started_before: int | None = None,
        expand: list[str] | None = None,
    ) -> WorklogPage:
        params: dict[str, str] = {
            "startAt": str(start_at),
            "maxResults": str(max_results),
        }
        if started_after is not None:
            params["startedAfter"] = str(started_after)
        if started_before is not None:
            params["startedBefore"] = str(started_before)
        if expand:
            params["expand"] = ",".join(expand)
        response = await self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/worklog",
            params=params,
        )
        raise_for_response(response)
        return WorklogPage.model_validate(response.json())

    async def add_worklog(
        self,
        issue_id_or_key: str,
        body: dict[str, Any],
        *,
        notify_users: bool = True,
        adjust_estimate: str | None = None,
        new_estimate: str | None = None,
        reduce_by: str | None = None,
        expand: list[str] | None = None,
        override_editable_flag: bool = False,
    ) -> Worklog:
        params: dict[str, str] = {}
        if not notify_users:
            params["notifyUsers"] = "false"
        if adjust_estimate:
            params["adjustEstimate"] = adjust_estimate
        if new_estimate:
            params["newEstimate"] = new_estimate
        if reduce_by:
            params["reduceBy"] = reduce_by
        if expand:
            params["expand"] = ",".join(expand)
        if override_editable_flag:
            params["overrideEditableFlag"] = "true"
        response = await self._client.post(
            f"/rest/api/3/issue/{issue_id_or_key}/worklog",
            json=body,
            params=params,
        )
        raise_for_response(response)
        return Worklog.model_validate(response.json())

    async def get_worklog(
        self,
        issue_id_or_key: str,
        worklog_id: str,
        *,
        expand: list[str] | None = None,
    ) -> Worklog:
        params: dict[str, str] = {}
        if expand:
            params["expand"] = ",".join(expand)
        response = await self._client.get(
            f"/rest/api/3/issue/{issue_id_or_key}/worklog/{worklog_id}",
            params=params,
        )
        raise_for_response(response)
        return Worklog.model_validate(response.json())

    async def update_worklog(
        self,
        issue_id_or_key: str,
        worklog_id: str,
        body: dict[str, Any],
        *,
        notify_users: bool = True,
        adjust_estimate: str | None = None,
        new_estimate: str | None = None,
        expand: list[str] | None = None,
        override_editable_flag: bool = False,
    ) -> Worklog:
        params: dict[str, str] = {}
        if not notify_users:
            params["notifyUsers"] = "false"
        if adjust_estimate:
            params["adjustEstimate"] = adjust_estimate
        if new_estimate:
            params["newEstimate"] = new_estimate
        if expand:
            params["expand"] = ",".join(expand)
        if override_editable_flag:
            params["overrideEditableFlag"] = "true"
        response = await self._client.put(
            f"/rest/api/3/issue/{issue_id_or_key}/worklog/{worklog_id}",
            json=body,
            params=params,
        )
        raise_for_response(response)
        return Worklog.model_validate(response.json())

    async def delete_worklog(
        self,
        issue_id_or_key: str,
        worklog_id: str,
        *,
        notify_users: bool = True,
        adjust_estimate: str | None = None,
        new_estimate: str | None = None,
        increase_by: str | None = None,
        override_editable_flag: bool = False,
    ) -> None:
        params: dict[str, str] = {}
        if not notify_users:
            params["notifyUsers"] = "false"
        if adjust_estimate:
            params["adjustEstimate"] = adjust_estimate
        if new_estimate:
            params["newEstimate"] = new_estimate
        if increase_by:
            params["increaseBy"] = increase_by
        if override_editable_flag:
            params["overrideEditableFlag"] = "true"
        response = await self._client.delete(
            f"/rest/api/3/issue/{issue_id_or_key}/worklog/{worklog_id}",
            params=params,
        )
        raise_for_response(response)
