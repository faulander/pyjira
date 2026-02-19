from __future__ import annotations

from typing import TYPE_CHECKING

from pyjira.exceptions import raise_for_response
from pyjira.models.user import User

if TYPE_CHECKING:
  import httpx


class UserResource:
  """Sync operations for Jira users."""

  def __init__(self, client: httpx.Client) -> None:
    self._client = client

  def get(self, account_id: str) -> User:
    response = self._client.get('/rest/api/3/user', params={'accountId': account_id})
    raise_for_response(response)
    return User.model_validate(response.json())

  def myself(self) -> User:
    response = self._client.get('/rest/api/3/myself')
    raise_for_response(response)
    return User.model_validate(response.json())

  def search(
    self,
    *,
    query: str | None = None,
    start_at: int = 0,
    max_results: int = 50,
  ) -> list[User]:
    params: dict[str, str] = {
      'startAt': str(start_at),
      'maxResults': str(max_results),
    }
    if query:
      params['query'] = query
    response = self._client.get('/rest/api/3/users/search', params=params)
    raise_for_response(response)
    return [User.model_validate(u) for u in response.json()]


class AsyncUserResource:
  """Async operations for Jira users."""

  def __init__(self, client: httpx.AsyncClient) -> None:
    self._client = client

  async def get(self, account_id: str) -> User:
    response = await self._client.get('/rest/api/3/user', params={'accountId': account_id})
    raise_for_response(response)
    return User.model_validate(response.json())

  async def myself(self) -> User:
    response = await self._client.get('/rest/api/3/myself')
    raise_for_response(response)
    return User.model_validate(response.json())

  async def search(
    self,
    *,
    query: str | None = None,
    start_at: int = 0,
    max_results: int = 50,
  ) -> list[User]:
    params: dict[str, str] = {
      'startAt': str(start_at),
      'maxResults': str(max_results),
    }
    if query:
      params['query'] = query
    response = await self._client.get('/rest/api/3/users/search', params=params)
    raise_for_response(response)
    return [User.model_validate(u) for u in response.json()]
