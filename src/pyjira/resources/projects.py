from __future__ import annotations

from typing import TYPE_CHECKING

from pyjira.exceptions import raise_for_response
from pyjira.models.project import Project

if TYPE_CHECKING:
  import httpx


class ProjectResource:
  """Sync operations for Jira projects."""

  def __init__(self, client: httpx.Client) -> None:
    self._client = client

  def list(
    self,
    *,
    expand: list[str] | None = None,
    recent: int | None = None,
    order_by: str | None = None,
  ) -> list[Project]:
    params: dict[str, str] = {}
    if expand:
      params['expand'] = ','.join(expand)
    if recent is not None:
      params['recent'] = str(recent)
    if order_by:
      params['orderBy'] = order_by
    response = self._client.get('/rest/api/3/project', params=params)
    raise_for_response(response)
    return [Project.model_validate(p) for p in response.json()]

  def get(
    self,
    project_id_or_key: str,
    *,
    expand: list[str] | None = None,
  ) -> Project:
    params: dict[str, str] = {}
    if expand:
      params['expand'] = ','.join(expand)
    response = self._client.get(f'/rest/api/3/project/{project_id_or_key}', params=params)
    raise_for_response(response)
    return Project.model_validate(response.json())


class AsyncProjectResource:
  """Async operations for Jira projects."""

  def __init__(self, client: httpx.AsyncClient) -> None:
    self._client = client

  async def list(
    self,
    *,
    expand: list[str] | None = None,
    recent: int | None = None,
    order_by: str | None = None,
  ) -> list[Project]:
    params: dict[str, str] = {}
    if expand:
      params['expand'] = ','.join(expand)
    if recent is not None:
      params['recent'] = str(recent)
    if order_by:
      params['orderBy'] = order_by
    response = await self._client.get('/rest/api/3/project', params=params)
    raise_for_response(response)
    return [Project.model_validate(p) for p in response.json()]

  async def get(
    self,
    project_id_or_key: str,
    *,
    expand: list[str] | None = None,
  ) -> Project:
    params: dict[str, str] = {}
    if expand:
      params['expand'] = ','.join(expand)
    response = await self._client.get(f'/rest/api/3/project/{project_id_or_key}', params=params)
    raise_for_response(response)
    return Project.model_validate(response.json())
