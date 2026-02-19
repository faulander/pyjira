import pytest
import respx

from pyjira import JiraClient


BASE_URL = 'https://test.atlassian.net'


@pytest.fixture
def mock_api():
  with respx.mock(base_url=BASE_URL) as respx_mock:
    yield respx_mock


@pytest.fixture
def client(mock_api):
  with JiraClient(
    base_url=BASE_URL,
    email='test@example.com',
    api_token='test-token',
  ) as c:
    yield c


ISSUE_JSON = {
  'id': '10001',
  'key': 'PROJ-123',
  'self': f'{BASE_URL}/rest/api/3/issue/10001',
  'fields': {
    'summary': 'Test issue',
    'description': None,
    'status': {
      'id': '1',
      'name': 'Open',
      'statusCategory': {
        'id': 2,
        'key': 'new',
        'name': 'To Do',
      },
    },
    'priority': {
      'id': '3',
      'name': 'Medium',
    },
    'issuetype': {
      'id': '10001',
      'name': 'Task',
      'subtask': False,
    },
    'assignee': {
      'accountId': 'abc123',
      'displayName': 'Test User',
      'emailAddress': 'test@example.com',
      'active': True,
    },
    'reporter': {
      'accountId': 'def456',
      'displayName': 'Reporter User',
      'active': True,
    },
    'project': {
      'id': '10000',
      'key': 'PROJ',
      'name': 'Test Project',
    },
    'created': '2025-01-15T10:30:00.000+0000',
    'updated': '2025-01-16T14:20:00.000+0000',
    'labels': ['bug', 'urgent'],
  },
}

PROJECT_JSON = {
  'id': '10000',
  'key': 'PROJ',
  'name': 'Test Project',
  'self': f'{BASE_URL}/rest/api/3/project/10000',
  'projectTypeKey': 'software',
  'simplified': False,
  'isPrivate': False,
  'lead': {
    'accountId': 'abc123',
    'displayName': 'Test User',
    'active': True,
  },
}

USER_JSON = {
  'accountId': 'abc123',
  'emailAddress': 'test@example.com',
  'displayName': 'Test User',
  'active': True,
  'timeZone': 'America/New_York',
  'accountType': 'atlassian',
}

SEARCH_RESULTS_JSON = {
  'startAt': 0,
  'maxResults': 50,
  'total': 1,
  'issues': [ISSUE_JSON],
}
