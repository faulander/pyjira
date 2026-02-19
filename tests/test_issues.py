import httpx
import pytest
import respx

from pyjira import AuthenticationError, NotFoundError
from tests.conftest import BASE_URL, ISSUE_JSON


def test_get_issue(client, mock_api):
  mock_api.get('/rest/api/3/issue/PROJ-123').mock(
    return_value=httpx.Response(200, json=ISSUE_JSON),
  )
  issue = client.issues.get('PROJ-123')
  assert issue.key == 'PROJ-123'
  assert issue.id == '10001'
  assert issue.fields is not None
  assert issue.fields.summary == 'Test issue'
  assert issue.fields.status is not None
  assert issue.fields.status.name == 'Open'
  assert issue.fields.assignee is not None
  assert issue.fields.assignee.display_name == 'Test User'
  assert issue.fields.labels == ['bug', 'urgent']


def test_get_issue_with_expand(client, mock_api):
  route = mock_api.get('/rest/api/3/issue/PROJ-123').mock(
    return_value=httpx.Response(200, json=ISSUE_JSON),
  )
  client.issues.get('PROJ-123', expand=['changelog', 'transitions'])
  request = route.calls.last.request
  assert 'expand=changelog%2Ctransitions' in str(request.url) or 'expand=changelog,transitions' in str(request.url)


def test_get_issue_with_fields(client, mock_api):
  route = mock_api.get('/rest/api/3/issue/PROJ-123').mock(
    return_value=httpx.Response(200, json=ISSUE_JSON),
  )
  client.issues.get('PROJ-123', fields=['summary', 'status'])
  request = route.calls.last.request
  assert 'fields=' in str(request.url)


def test_get_issue_not_found(client, mock_api):
  mock_api.get('/rest/api/3/issue/INVALID').mock(
    return_value=httpx.Response(
      404,
      json={'errorMessages': ['Issue does not exist'], 'errors': {}},
    ),
  )
  with pytest.raises(NotFoundError) as exc_info:
    client.issues.get('INVALID')
  assert exc_info.value.status_code == 404
  assert 'Issue does not exist' in str(exc_info.value)


def test_get_issue_unauthorized(client, mock_api):
  mock_api.get('/rest/api/3/issue/PROJ-1').mock(
    return_value=httpx.Response(
      401,
      json={'errorMessages': ['Authentication required'], 'errors': {}},
    ),
  )
  with pytest.raises(AuthenticationError):
    client.issues.get('PROJ-1')


def test_create_issue(client, mock_api):
  created = {**ISSUE_JSON, 'key': 'PROJ-124', 'id': '10002'}
  mock_api.post('/rest/api/3/issue').mock(
    return_value=httpx.Response(201, json=created),
  )
  issue = client.issues.create(
    fields={
      'project': {'key': 'PROJ'},
      'summary': 'New issue',
      'issuetype': {'name': 'Task'},
    },
  )
  assert issue.key == 'PROJ-124'


def test_update_issue(client, mock_api):
  mock_api.put('/rest/api/3/issue/PROJ-123').mock(
    return_value=httpx.Response(204),
  )
  client.issues.update('PROJ-123', fields={'summary': 'Updated'})


def test_delete_issue(client, mock_api):
  mock_api.delete('/rest/api/3/issue/PROJ-123').mock(
    return_value=httpx.Response(204),
  )
  client.issues.delete('PROJ-123')


def test_get_transitions(client, mock_api):
  mock_api.get('/rest/api/3/issue/PROJ-123/transitions').mock(
    return_value=httpx.Response(200, json={
      'transitions': [
        {'id': '11', 'name': 'In Progress', 'to': {'id': '3', 'name': 'In Progress'}},
        {'id': '21', 'name': 'Done', 'to': {'id': '5', 'name': 'Done'}},
      ],
    }),
  )
  transitions = client.issues.get_transitions('PROJ-123')
  assert len(transitions) == 2
  assert transitions[0].name == 'In Progress'
  assert transitions[1].id == '21'


def test_transition_issue(client, mock_api):
  mock_api.post('/rest/api/3/issue/PROJ-123/transitions').mock(
    return_value=httpx.Response(204),
  )
  client.issues.transition('PROJ-123', '11')
