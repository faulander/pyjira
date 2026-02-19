from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field

from pyjira.exceptions import raise_for_response
from pyjira.models.comment import Comment
from pyjira.models.common import PaginatedResponse

if TYPE_CHECKING:
  import httpx


class CommentPage(PaginatedResponse):
  comments: list[Comment] = Field(default_factory=list)


class CommentResource:
  """Sync operations for issue comments."""

  def __init__(self, client: httpx.Client) -> None:
    self._client = client

  def list(
    self,
    issue_id_or_key: str,
    *,
    start_at: int = 0,
    max_results: int = 50,
    order_by: str | None = None,
    expand: list[str] | None = None,
  ) -> CommentPage:
    params: dict[str, str] = {
      'startAt': str(start_at),
      'maxResults': str(max_results),
    }
    if order_by:
      params['orderBy'] = order_by
    if expand:
      params['expand'] = ','.join(expand)
    response = self._client.get(
      f'/rest/api/3/issue/{issue_id_or_key}/comment',
      params=params,
    )
    raise_for_response(response)
    return CommentPage.model_validate(response.json())

  def get(self, issue_id_or_key: str, comment_id: str) -> Comment:
    response = self._client.get(
      f'/rest/api/3/issue/{issue_id_or_key}/comment/{comment_id}',
    )
    raise_for_response(response)
    return Comment.model_validate(response.json())

  def add(
    self,
    issue_id_or_key: str,
    body: Any,
    *,
    visibility: dict[str, str] | None = None,
  ) -> Comment:
    payload: dict[str, Any] = {'body': body}
    if visibility:
      payload['visibility'] = visibility
    response = self._client.post(
      f'/rest/api/3/issue/{issue_id_or_key}/comment',
      json=payload,
    )
    raise_for_response(response)
    return Comment.model_validate(response.json())

  def update(
    self,
    issue_id_or_key: str,
    comment_id: str,
    body: Any,
    *,
    visibility: dict[str, str] | None = None,
  ) -> Comment:
    payload: dict[str, Any] = {'body': body}
    if visibility:
      payload['visibility'] = visibility
    response = self._client.put(
      f'/rest/api/3/issue/{issue_id_or_key}/comment/{comment_id}',
      json=payload,
    )
    raise_for_response(response)
    return Comment.model_validate(response.json())

  def delete(self, issue_id_or_key: str, comment_id: str) -> None:
    response = self._client.delete(
      f'/rest/api/3/issue/{issue_id_or_key}/comment/{comment_id}',
    )
    raise_for_response(response)


class AsyncCommentResource:
  """Async operations for issue comments."""

  def __init__(self, client: httpx.AsyncClient) -> None:
    self._client = client

  async def list(
    self,
    issue_id_or_key: str,
    *,
    start_at: int = 0,
    max_results: int = 50,
    order_by: str | None = None,
    expand: list[str] | None = None,
  ) -> CommentPage:
    params: dict[str, str] = {
      'startAt': str(start_at),
      'maxResults': str(max_results),
    }
    if order_by:
      params['orderBy'] = order_by
    if expand:
      params['expand'] = ','.join(expand)
    response = await self._client.get(
      f'/rest/api/3/issue/{issue_id_or_key}/comment',
      params=params,
    )
    raise_for_response(response)
    return CommentPage.model_validate(response.json())

  async def get(self, issue_id_or_key: str, comment_id: str) -> Comment:
    response = await self._client.get(
      f'/rest/api/3/issue/{issue_id_or_key}/comment/{comment_id}',
    )
    raise_for_response(response)
    return Comment.model_validate(response.json())

  async def add(
    self,
    issue_id_or_key: str,
    body: Any,
    *,
    visibility: dict[str, str] | None = None,
  ) -> Comment:
    payload: dict[str, Any] = {'body': body}
    if visibility:
      payload['visibility'] = visibility
    response = await self._client.post(
      f'/rest/api/3/issue/{issue_id_or_key}/comment',
      json=payload,
    )
    raise_for_response(response)
    return Comment.model_validate(response.json())

  async def update(
    self,
    issue_id_or_key: str,
    comment_id: str,
    body: Any,
    *,
    visibility: dict[str, str] | None = None,
  ) -> Comment:
    payload: dict[str, Any] = {'body': body}
    if visibility:
      payload['visibility'] = visibility
    response = await self._client.put(
      f'/rest/api/3/issue/{issue_id_or_key}/comment/{comment_id}',
      json=payload,
    )
    raise_for_response(response)
    return Comment.model_validate(response.json())

  async def delete(self, issue_id_or_key: str, comment_id: str) -> None:
    response = await self._client.delete(
      f'/rest/api/3/issue/{issue_id_or_key}/comment/{comment_id}',
    )
    raise_for_response(response)
