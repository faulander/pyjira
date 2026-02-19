import httpx
import pytest
import respx

from tests.conftest import BASE_URL, ISSUE_JSON, SEARCH_RESULTS_JSON


def test_jql_search(client, mock_api):
  mock_api.get('/rest/api/3/search').mock(
    return_value=httpx.Response(200, json=SEARCH_RESULTS_JSON),
  )
  results = client.search.jql('project = PROJ')
  assert results.total == 1
  assert len(results.issues) == 1
  assert results.issues[0].key == 'PROJ-123'
  assert results.start_at == 0
  assert results.max_results == 50


def test_jql_search_with_params(client, mock_api):
  route = mock_api.get('/rest/api/3/search').mock(
    return_value=httpx.Response(200, json=SEARCH_RESULTS_JSON),
  )
  client.search.jql(
    'project = PROJ',
    start_at=10,
    max_results=25,
    fields=['summary', 'status'],
    expand=['changelog'],
  )
  request = route.calls.last.request
  url = str(request.url)
  assert 'startAt=10' in url
  assert 'maxResults=25' in url
  assert 'fields=' in url
  assert 'expand=changelog' in url


def test_jql_search_empty_results(client, mock_api):
  mock_api.get('/rest/api/3/search').mock(
    return_value=httpx.Response(200, json={
      'startAt': 0,
      'maxResults': 50,
      'total': 0,
      'issues': [],
    }),
  )
  results = client.search.jql('project = EMPTY')
  assert results.total == 0
  assert len(results.issues) == 0
