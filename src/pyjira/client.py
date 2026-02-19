from __future__ import annotations

import httpx

from pyjira.auth import build_auth
from pyjira.config import JiraConfig
from pyjira.resources.attachments import (
    AsyncAttachmentResource,
    AttachmentResource,
)
from pyjira.resources.comments import AsyncCommentResource, CommentResource
from pyjira.resources.components import (
    AsyncComponentResource,
    ComponentResource,
)
from pyjira.resources.dashboards import (
    AsyncDashboardResource,
    DashboardResource,
)
from pyjira.resources.fields import AsyncFieldResource, FieldResource
from pyjira.resources.filters import AsyncFilterResource, FilterResource
from pyjira.resources.groups import AsyncGroupResource, GroupResource
from pyjira.resources.issue_links import (
    AsyncIssueLinkResource,
    IssueLinkResource,
)
from pyjira.resources.issue_types import (
    AsyncIssueTypeResource,
    IssueTypeResource,
)
from pyjira.resources.issues import AsyncIssueResource, IssueResource
from pyjira.resources.notification_schemes import (
    AsyncNotificationSchemeResource,
    NotificationSchemeResource,
)
from pyjira.resources.permissions import (
    AsyncPermissionResource,
    PermissionResource,
)
from pyjira.resources.priorities import (
    AsyncPriorityResource,
    PriorityResource,
)
from pyjira.resources.projects import AsyncProjectResource, ProjectResource
from pyjira.resources.resolutions import (
    AsyncResolutionResource,
    ResolutionResource,
)
from pyjira.resources.roles import AsyncRoleResource, RoleResource
from pyjira.resources.screens import AsyncScreenResource, ScreenResource
from pyjira.resources.search import AsyncSearchResource, SearchResource
from pyjira.resources.server_info import (
    AsyncServerInfoResource,
    ServerInfoResource,
)
from pyjira.resources.statuses import AsyncStatusResource, StatusResource
from pyjira.resources.users import AsyncUserResource, UserResource
from pyjira.resources.versions import AsyncVersionResource, VersionResource
from pyjira.resources.workflows import (
    AsyncWorkflowResource,
    WorkflowResource,
)

_DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


class JiraClient:
    """Synchronous Jira REST API v3 client.

    Usage:
      client = JiraClient(
        domain='mycompany',
        email='user@example.com',
        api_token='your-api-token',
      )
      issue = client.issues.get('PROJ-123')
    """

    def __init__(
        self,
        *,
        domain: str | None = None,
        base_url: str | None = None,
        email: str,
        api_token: str,
        timeout: float = 30.0,
        headers: dict[str, str] | None = None,
    ) -> None:
        if domain:
            resolved_base_url = f"https://{domain}.atlassian.net"
        elif base_url:
            resolved_base_url = base_url.rstrip("/")
        else:
            raise ValueError("Either domain or base_url must be provided")

        self._config = JiraConfig(
            base_url=resolved_base_url,
            email=email,
            api_token=api_token,
            timeout=timeout,
        )

        merged_headers = {**_DEFAULT_HEADERS, **(headers or {})}
        auth = build_auth(email, api_token)

        self._http = httpx.Client(
            base_url=resolved_base_url,
            auth=auth,
            headers=merged_headers,
            timeout=timeout,
        )

        self.attachments = AttachmentResource(self._http)
        self.comments = CommentResource(self._http)
        self.components = ComponentResource(self._http)
        self.dashboards = DashboardResource(self._http)
        self.fields = FieldResource(self._http)
        self.filters = FilterResource(self._http)
        self.groups = GroupResource(self._http)
        self.issue_links = IssueLinkResource(self._http)
        self.issue_types = IssueTypeResource(self._http)
        self.issues = IssueResource(self._http)
        self.notification_schemes = NotificationSchemeResource(self._http)
        self.permissions = PermissionResource(self._http)
        self.priorities = PriorityResource(self._http)
        self.projects = ProjectResource(self._http)
        self.resolutions = ResolutionResource(self._http)
        self.roles = RoleResource(self._http)
        self.screens = ScreenResource(self._http)
        self.search = SearchResource(self._http)
        self.server_info = ServerInfoResource(self._http)
        self.statuses = StatusResource(self._http)
        self.users = UserResource(self._http)
        self.versions = VersionResource(self._http)
        self.workflows = WorkflowResource(self._http)

    @property
    def config(self) -> JiraConfig:
        return self._config

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> JiraClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncJiraClient:
    """Asynchronous Jira REST API v3 client.

    Usage:
      async with AsyncJiraClient(
        domain='mycompany',
        email='user@example.com',
        api_token='your-api-token',
      ) as client:
        issue = await client.issues.get('PROJ-123')
    """

    def __init__(
        self,
        *,
        domain: str | None = None,
        base_url: str | None = None,
        email: str,
        api_token: str,
        timeout: float = 30.0,
        headers: dict[str, str] | None = None,
    ) -> None:
        if domain:
            resolved_base_url = f"https://{domain}.atlassian.net"
        elif base_url:
            resolved_base_url = base_url.rstrip("/")
        else:
            raise ValueError("Either domain or base_url must be provided")

        self._config = JiraConfig(
            base_url=resolved_base_url,
            email=email,
            api_token=api_token,
            timeout=timeout,
        )

        merged_headers = {**_DEFAULT_HEADERS, **(headers or {})}
        auth = build_auth(email, api_token)

        self._http = httpx.AsyncClient(
            base_url=resolved_base_url,
            auth=auth,
            headers=merged_headers,
            timeout=timeout,
        )

        self.attachments = AsyncAttachmentResource(self._http)
        self.comments = AsyncCommentResource(self._http)
        self.components = AsyncComponentResource(self._http)
        self.dashboards = AsyncDashboardResource(self._http)
        self.fields = AsyncFieldResource(self._http)
        self.filters = AsyncFilterResource(self._http)
        self.groups = AsyncGroupResource(self._http)
        self.issue_links = AsyncIssueLinkResource(self._http)
        self.issue_types = AsyncIssueTypeResource(self._http)
        self.issues = AsyncIssueResource(self._http)
        self.notification_schemes = AsyncNotificationSchemeResource(self._http)
        self.permissions = AsyncPermissionResource(self._http)
        self.priorities = AsyncPriorityResource(self._http)
        self.projects = AsyncProjectResource(self._http)
        self.resolutions = AsyncResolutionResource(self._http)
        self.roles = AsyncRoleResource(self._http)
        self.screens = AsyncScreenResource(self._http)
        self.search = AsyncSearchResource(self._http)
        self.server_info = AsyncServerInfoResource(self._http)
        self.statuses = AsyncStatusResource(self._http)
        self.users = AsyncUserResource(self._http)
        self.versions = AsyncVersionResource(self._http)
        self.workflows = AsyncWorkflowResource(self._http)

    @property
    def config(self) -> JiraConfig:
        return self._config

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> AsyncJiraClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
