from __future__ import annotations

from typing import TYPE_CHECKING

from pyjira.exceptions import raise_for_response
from pyjira.models.issue import Issue
from pyjira.models.search import SearchResults
from pyjira.pagination import AsyncPaginator, Paginator

if TYPE_CHECKING:
  import httpx


class SearchResource:
  """Sync JQL search operations."""

  def __init__(self, client: httpx.Client) -> None:
    self._client = client

  def jql(
    self,
    jql: str,
    *,
    start_at: int = 0,
    max_results: int = 50,
    fields: list[str] | None = None,
    expand: list[str] | None = None,
    validate_query: str | None = None,
  ) -> SearchResults:
    params: dict[str, str] = {
      'jql': jql,
      'startAt': str(start_at),
      'maxResults': str(max_results),
    }
    if fields:
      params['fields'] = ','.join(fields)
    if expand:
      params['expand'] = ','.join(expand)
    if validate_query:
      params['validateQuery'] = validate_query
    response = self._client.get('/rest/api/3/search', params=params)
    raise_for_response(response)
    return SearchResults.model_validate(response.json())

  def jql_paginated(
    self,
    jql: str,
    *,
    page_size: int = 50,
    fields: list[str] | None = None,
    expand: list[str] | None = None,
  ) -> Paginator[Issue]:
    def fetch_page(start_at: int, max_results: int) -> tuple[list[Issue], int]:
      results = self.jql(
        jql,
        start_at=start_at,
        max_results=max_results,
        fields=fields,
        expand=expand,
      )
      return results.issues, results.total

    return Paginator(fetch_page, page_size=page_size)


class AsyncSearchResource:
  """Async JQL search operations."""

  def __init__(self, client: httpx.AsyncClient) -> None:
    self._client = client

  async def jql(
    self,
    jql: str,
    *,
    start_at: int = 0,
    max_results: int = 50,
    fields: list[str] | None = None,
    expand: list[str] | None = None,
    validate_query: str | None = None,
  ) -> SearchResults:
    params: dict[str, str] = {
      'jql': jql,
      'startAt': str(start_at),
      'maxResults': str(max_results),
    }
    if fields:
      params['fields'] = ','.join(fields)
    if expand:
      params['expand'] = ','.join(expand)
    if validate_query:
      params['validateQuery'] = validate_query
    response = await self._client.get('/rest/api/3/search', params=params)
    raise_for_response(response)
    return SearchResults.model_validate(response.json())

  def jql_paginated(
    self,
    jql: str,
    *,
    page_size: int = 50,
    fields: list[str] | None = None,
    expand: list[str] | None = None,
  ) -> AsyncPaginator[Issue]:
    async def fetch_page(start_at: int, max_results: int) -> tuple[list[Issue], int]:
      results = await self.jql(
        jql,
        start_at=start_at,
        max_results=max_results,
        fields=fields,
        expand=expand,
      )
      return results.issues, results.total

    return AsyncPaginator(fetch_page, page_size=page_size)
