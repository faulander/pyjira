import httpx
import pytest
import respx

from pyjira.models.issue import Issue
from pyjira.pagination import AsyncPaginator, Paginator
from tests.conftest import BASE_URL, ISSUE_JSON


def _make_issue(key: str) -> Issue:
  return Issue.model_validate({**ISSUE_JSON, 'key': key})


def test_paginator_single_page():
  items = [_make_issue(f'PROJ-{i}') for i in range(3)]

  def fetch_page(start_at: int, max_results: int) -> tuple[list[Issue], int]:
    return items, 3

  paginator = Paginator(fetch_page, page_size=50)
  results = list(paginator)
  assert len(results) == 3
  assert results[0].key == 'PROJ-0'
  assert results[2].key == 'PROJ-2'


def test_paginator_multiple_pages():
  all_items = [_make_issue(f'PROJ-{i}') for i in range(5)]

  def fetch_page(start_at: int, max_results: int) -> tuple[list[Issue], int]:
    page = all_items[start_at:start_at + max_results]
    return page, 5

  paginator = Paginator(fetch_page, page_size=2)
  results = list(paginator)
  assert len(results) == 5
  assert [r.key for r in results] == [f'PROJ-{i}' for i in range(5)]


def test_paginator_empty():
  def fetch_page(start_at: int, max_results: int) -> tuple[list[Issue], int]:
    return [], 0

  paginator = Paginator(fetch_page, page_size=50)
  results = list(paginator)
  assert results == []


def test_jql_paginated_integration(client, mock_api):
  page1 = {
    'startAt': 0,
    'maxResults': 2,
    'total': 3,
    'issues': [
      {**ISSUE_JSON, 'key': 'PROJ-1'},
      {**ISSUE_JSON, 'key': 'PROJ-2'},
    ],
  }
  page2 = {
    'startAt': 2,
    'maxResults': 2,
    'total': 3,
    'issues': [
      {**ISSUE_JSON, 'key': 'PROJ-3'},
    ],
  }

  call_count = 0

  def side_effect(request: httpx.Request) -> httpx.Response:
    nonlocal call_count
    call_count += 1
    if call_count == 1:
      return httpx.Response(200, json=page1)
    return httpx.Response(200, json=page2)

  mock_api.get('/rest/api/3/search').mock(side_effect=side_effect)

  issues = list(client.search.jql_paginated('project = PROJ', page_size=2))
  assert len(issues) == 3
  assert issues[0].key == 'PROJ-1'
  assert issues[1].key == 'PROJ-2'
  assert issues[2].key == 'PROJ-3'


@pytest.mark.asyncio
async def test_async_paginator_single_page():
  items = [_make_issue(f'PROJ-{i}') for i in range(3)]

  async def fetch_page(start_at: int, max_results: int) -> tuple[list[Issue], int]:
    return items, 3

  paginator = AsyncPaginator(fetch_page, page_size=50)
  results = [item async for item in paginator]
  assert len(results) == 3


@pytest.mark.asyncio
async def test_async_paginator_multiple_pages():
  all_items = [_make_issue(f'PROJ-{i}') for i in range(5)]

  async def fetch_page(start_at: int, max_results: int) -> tuple[list[Issue], int]:
    page = all_items[start_at:start_at + max_results]
    return page, 5

  paginator = AsyncPaginator(fetch_page, page_size=2)
  results = [item async for item in paginator]
  assert len(results) == 5
