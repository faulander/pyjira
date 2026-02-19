from __future__ import annotations

import httpx

from pyjira.auth import build_auth
from pyjira.config import JiraConfig
from pyjira.resources.comments import AsyncCommentResource, CommentResource
from pyjira.resources.issues import AsyncIssueResource, IssueResource
from pyjira.resources.projects import AsyncProjectResource, ProjectResource
from pyjira.resources.search import AsyncSearchResource, SearchResource
from pyjira.resources.users import AsyncUserResource, UserResource


_DEFAULT_HEADERS = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
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
      resolved_base_url = f'https://{domain}.atlassian.net'
    elif base_url:
      resolved_base_url = base_url.rstrip('/')
    else:
      raise ValueError('Either domain or base_url must be provided')

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

    self.issues = IssueResource(self._http)
    self.projects = ProjectResource(self._http)
    self.search = SearchResource(self._http)
    self.users = UserResource(self._http)
    self.comments = CommentResource(self._http)

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
      resolved_base_url = f'https://{domain}.atlassian.net'
    elif base_url:
      resolved_base_url = base_url.rstrip('/')
    else:
      raise ValueError('Either domain or base_url must be provided')

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

    self.issues = AsyncIssueResource(self._http)
    self.projects = AsyncProjectResource(self._http)
    self.search = AsyncSearchResource(self._http)
    self.users = AsyncUserResource(self._http)
    self.comments = AsyncCommentResource(self._http)

  @property
  def config(self) -> JiraConfig:
    return self._config

  async def close(self) -> None:
    await self._http.aclose()

  async def __aenter__(self) -> AsyncJiraClient:
    return self

  async def __aexit__(self, *args: object) -> None:
    await self.close()
