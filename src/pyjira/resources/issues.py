from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyjira.exceptions import raise_for_response
from pyjira.models.issue import Issue, Transition

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
    params['fields'] = ','.join(fields)
  if expand:
    params['expand'] = ','.join(expand)
  if properties:
    params['properties'] = ','.join(properties)
  return params


class IssueResource:
  """Sync operations for Jira issues."""

  def __init__(self, client: httpx.Client) -> None:
    self._client = client

  def get(
    self,
    issue_id_or_key: str,
    *,
    fields: list[str] | None = None,
    expand: list[str] | None = None,
    properties: list[str] | None = None,
  ) -> Issue:
    params = _build_params(fields=fields, expand=expand, properties=properties)
    response = self._client.get(f'/rest/api/3/issue/{issue_id_or_key}', params=params)
    raise_for_response(response)
    return Issue.model_validate(response.json())

  def create(
    self,
    fields: dict[str, Any],
    *,
    update: dict[str, Any] | None = None,
  ) -> Issue:
    body: dict[str, Any] = {'fields': fields}
    if update:
      body['update'] = update
    response = self._client.post('/rest/api/3/issue', json=body)
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
      body['fields'] = fields
    if update:
      body['update'] = update
    params = {} if notify_users else {'notifyUsers': 'false'}
    response = self._client.put(
      f'/rest/api/3/issue/{issue_id_or_key}',
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
    params = {'deleteSubtasks': str(delete_subtasks).lower()}
    response = self._client.delete(
      f'/rest/api/3/issue/{issue_id_or_key}',
      params=params,
    )
    raise_for_response(response)

  def get_transitions(
    self,
    issue_id_or_key: str,
    *,
    expand: list[str] | None = None,
  ) -> list[Transition]:
    params: dict[str, str] = {}
    if expand:
      params['expand'] = ','.join(expand)
    response = self._client.get(
      f'/rest/api/3/issue/{issue_id_or_key}/transitions',
      params=params,
    )
    raise_for_response(response)
    data = response.json()
    return [Transition.model_validate(t) for t in data.get('transitions', [])]

  def transition(
    self,
    issue_id_or_key: str,
    transition_id: str,
    *,
    fields: dict[str, Any] | None = None,
    update: dict[str, Any] | None = None,
    comment: dict[str, Any] | None = None,
  ) -> None:
    body: dict[str, Any] = {'transition': {'id': transition_id}}
    if fields:
      body['fields'] = fields
    if update:
      body['update'] = update
    if comment:
      body['update'] = body.get('update', {})
      body['update']['comment'] = [{'add': {'body': comment}}]
    response = self._client.post(
      f'/rest/api/3/issue/{issue_id_or_key}/transitions',
      json=body,
    )
    raise_for_response(response)


class AsyncIssueResource:
  """Async operations for Jira issues."""

  def __init__(self, client: httpx.AsyncClient) -> None:
    self._client = client

  async def get(
    self,
    issue_id_or_key: str,
    *,
    fields: list[str] | None = None,
    expand: list[str] | None = None,
    properties: list[str] | None = None,
  ) -> Issue:
    params = _build_params(fields=fields, expand=expand, properties=properties)
    response = await self._client.get(f'/rest/api/3/issue/{issue_id_or_key}', params=params)
    raise_for_response(response)
    return Issue.model_validate(response.json())

  async def create(
    self,
    fields: dict[str, Any],
    *,
    update: dict[str, Any] | None = None,
  ) -> Issue:
    body: dict[str, Any] = {'fields': fields}
    if update:
      body['update'] = update
    response = await self._client.post('/rest/api/3/issue', json=body)
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
      body['fields'] = fields
    if update:
      body['update'] = update
    params = {} if notify_users else {'notifyUsers': 'false'}
    response = await self._client.put(
      f'/rest/api/3/issue/{issue_id_or_key}',
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
    params = {'deleteSubtasks': str(delete_subtasks).lower()}
    response = await self._client.delete(
      f'/rest/api/3/issue/{issue_id_or_key}',
      params=params,
    )
    raise_for_response(response)

  async def get_transitions(
    self,
    issue_id_or_key: str,
    *,
    expand: list[str] | None = None,
  ) -> list[Transition]:
    params: dict[str, str] = {}
    if expand:
      params['expand'] = ','.join(expand)
    response = await self._client.get(
      f'/rest/api/3/issue/{issue_id_or_key}/transitions',
      params=params,
    )
    raise_for_response(response)
    data = response.json()
    return [Transition.model_validate(t) for t in data.get('transitions', [])]

  async def transition(
    self,
    issue_id_or_key: str,
    transition_id: str,
    *,
    fields: dict[str, Any] | None = None,
    update: dict[str, Any] | None = None,
    comment: dict[str, Any] | None = None,
  ) -> None:
    body: dict[str, Any] = {'transition': {'id': transition_id}}
    if fields:
      body['fields'] = fields
    if update:
      body['update'] = update
    if comment:
      body['update'] = body.get('update', {})
      body['update']['comment'] = [{'add': {'body': comment}}]
    response = await self._client.post(
      f'/rest/api/3/issue/{issue_id_or_key}/transitions',
      json=body,
    )
    raise_for_response(response)
