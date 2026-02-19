# pyJiraV3

[![Documentation Status](https://readthedocs.org/projects/pyjirav3/badge/?version=latest)](https://pyjirav3.readthedocs.io/en/latest/index.html)

A modern, fully-typed Python client for the [Jira Cloud REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/).

📖 **[Full Documentation](https://pyjirav3.readthedocs.io/en/latest/index.html)**

Built on [httpx](https://www.python-httpx.org/) and [Pydantic v2](https://docs.pydantic.dev/latest/). Supports both synchronous and asynchronous usage.

## Features

- **23 resource types** covering the full Jira Cloud REST API v3
- **Sync + async** -- every method works with both `httpx.Client` and `httpx.AsyncClient`
- **Fully typed** -- Pydantic v2 models with snake_case attributes and camelCase aliases
- **Auto-pagination** -- built-in `Paginator` / `AsyncPaginator` iterators
- **Typed exceptions** -- structured error hierarchy mapped from HTTP status codes
- **Extensible models** -- `extra='allow'` preserves unknown fields (custom fields, new API additions)

## Requirements

- Python 3.12+
- A Jira Cloud instance with an [API token](https://id.atlassian.com/manage/api-tokens)

## Installation

```bash
uv add pyjiraV3
```

Or with pip:

```bash
pip install pyjiraV3
```

Or install from source:

```bash
git clone https://github.com/faulander/pyjira.git
cd pyjira
uv sync
```

## Quick Start

```python
from pyjira import JiraClient

client = JiraClient(
  domain='mycompany',
  email='you@example.com',
  api_token='your-api-token',
)

issue = client.issues.get('PROJ-123')
print(issue.key, issue.fields.summary)

client.close()
```

Use as a context manager to close the underlying connection pool automatically:

```python
with JiraClient(domain='mycompany', email='you@example.com', api_token='tok') as client:
  issue = client.issues.get('PROJ-123')
```

### Async

```python
import asyncio
from pyjira import AsyncJiraClient

async def main():
  async with AsyncJiraClient(
    domain='mycompany',
    email='you@example.com',
    api_token='your-api-token',
  ) as client:
    issue = await client.issues.get('PROJ-123')
    print(issue.key)

asyncio.run(main())
```

Every sync method has an identical async counterpart. The examples below show the sync API; prefix with `await` for async.

## Authentication

pyJira uses Jira Cloud's [Basic auth with API tokens](https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/). Generate a token at https://id.atlassian.com/manage/api-tokens.

```python
# By Atlassian domain name (resolves to https://mycompany.atlassian.net)
client = JiraClient(domain='mycompany', email='...', api_token='...')

# By explicit base URL (for custom domains or proxies)
client = JiraClient(base_url='https://jira.internal.company.com', email='...', api_token='...')
```

You must provide either `domain` or `base_url`, not both.

### Client Options

| Parameter   | Type              | Default | Description                                |
|-------------|-------------------|---------|--------------------------------------------|
| `domain`    | `str \| None`     | `None`  | Atlassian domain (e.g. `'mycompany'`)      |
| `base_url`  | `str \| None`     | `None`  | Full base URL (alternative to `domain`)    |
| `email`     | `str`             | -       | Atlassian account email                    |
| `api_token` | `str`             | -       | API token from Atlassian account settings  |
| `timeout`   | `float`           | `30.0`  | Request timeout in seconds                 |
| `headers`   | `dict \| None`    | `None`  | Additional HTTP headers to merge in        |

## Resources

The client exposes 23 resource attributes, each mapping to a Jira API group:

| Resource | Attribute | Description |
|----------|-----------|-------------|
| **Issues** | `client.issues` | Issue CRUD, transitions, attachments, worklogs, watchers, votes, remote links, properties |
| **Search** | `client.search` | JQL search with manual and auto-pagination |
| **Projects** | `client.projects` | Project listing and details |
| **Users** | `client.users` | User lookup and search |
| **Comments** | `client.comments` | Issue comment CRUD |
| **Attachments** | `client.attachments` | Attachment metadata, content, thumbnails |
| **Components** | `client.components` | Project component CRUD |
| **Dashboards** | `client.dashboards` | Dashboard and gadget management |
| **Fields** | `client.fields` | Field CRUD, search, trash/restore |
| **Filters** | `client.filters` | Saved filter CRUD, sharing, favorites |
| **Groups** | `client.groups` | Group CRUD, membership management |
| **Issue Links** | `client.issue_links` | Issue link and link type management |
| **Issue Types** | `client.issue_types` | Issue type CRUD, properties |
| **Notification Schemes** | `client.notification_schemes` | Notification scheme management |
| **Permissions** | `client.permissions` | Permission and scheme management |
| **Priorities** | `client.priorities` | Priority CRUD, ordering |
| **Resolutions** | `client.resolutions` | Resolution CRUD, ordering |
| **Roles** | `client.roles` | Project role and actor management |
| **Screens** | `client.screens` | Screen, tab, and field management |
| **Server Info** | `client.server_info` | Jira server info and configuration |
| **Statuses** | `client.statuses` | Status CRUD and search |
| **Versions** | `client.versions` | Version CRUD, merge, move |
| **Workflows** | `client.workflows` | Workflow and scheme management |

> For detailed documentation on every resource and method, see the [full documentation](https://pyjirav3.readthedocs.io/en/latest/index.html).

---

### Issues

#### Get an issue

```python
issue = client.issues.get('PROJ-123')

print(issue.key)                           # 'PROJ-123'
print(issue.fields.summary)                # 'Fix login bug'
print(issue.fields.status.name)            # 'In Progress'
print(issue.fields.assignee.display_name)  # 'Jane Doe'
print(issue.fields.priority.name)          # 'High'
print(issue.fields.labels)                 # ['bug', 'auth']
```

Use `fields` to limit which fields are returned and `expand` to include additional data:

```python
issue = client.issues.get(
  'PROJ-123',
  fields=['summary', 'status', 'assignee'],
  expand=['changelog', 'transitions'],
)
```

#### Create an issue

```python
issue = client.issues.create(fields={
  'project': {'key': 'PROJ'},
  'summary': 'New bug report',
  'issuetype': {'name': 'Bug'},
  'description': {
    'type': 'doc',
    'version': 1,
    'content': [{
      'type': 'paragraph',
      'content': [{'type': 'text', 'text': 'Steps to reproduce...'}],
    }],
  },
})

print(issue.key)  # 'PROJ-456'
```

> **Note:** Jira API v3 uses [Atlassian Document Format (ADF)](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/) for rich text fields like `description` and comment bodies.

#### Update an issue

```python
client.issues.update('PROJ-123', fields={
  'summary': 'Updated summary',
  'priority': {'name': 'Critical'},
})

# Array field operations
client.issues.update('PROJ-123', update={
  'labels': [{'add': 'urgent'}, {'remove': 'low-priority'}],
})
```

#### Delete an issue

```python
client.issues.delete('PROJ-123', delete_subtasks=True)
```

#### Transitions

```python
transitions = client.issues.get_transitions('PROJ-123')
for t in transitions:
  print(f'{t.id}: {t.name} -> {t.to.name}')

client.issues.transition('PROJ-123', transition_id='31')
```

#### Attachments, Worklogs, Watchers, Votes

```python
# Add attachment
client.issues.add_attachment('PROJ-123', file_path='/path/to/file.pdf')

# Worklogs
client.issues.add_worklog('PROJ-123', body={'timeSpent': '2h'})
worklogs = client.issues.get_worklogs('PROJ-123')

# Watchers
watchers = client.issues.get_watchers('PROJ-123')
client.issues.add_watcher('PROJ-123', account_id='...')

# Votes
client.issues.add_vote('PROJ-123')
votes = client.issues.get_votes('PROJ-123')
```

---

### Search (JQL)

```python
results = client.search.jql('project = PROJ AND status = "In Progress"')
for issue in results.issues:
  print(issue.key, issue.fields.summary)
```

#### Auto-paginated search

```python
for issue in client.search.jql_paginated('project = PROJ', page_size=100):
  print(issue.key)

# Async
async for issue in client.search.jql_paginated('project = PROJ'):
  print(issue.key)
```

---

### Projects

```python
projects = client.projects.list()
project = client.projects.get('PROJ')
print(project.name, project.lead.display_name)
```

---

### More Resources

For detailed usage of all 23 resources including components, dashboards, filters, groups, permissions, priorities, resolutions, roles, screens, statuses, versions, workflows, and more, see the **[full documentation](https://pyjirav3.readthedocs.io/en/latest/index.html)**.

---

## Error Handling

All API errors raise typed exceptions:

```python
from pyjira import (
  JiraError,
  AuthenticationError,
  ForbiddenError,
  NotFoundError,
  ValidationError,
  RateLimitError,
  ServerError,
)

try:
  client.issues.get('INVALID-999')
except NotFoundError as e:
  print(e.status_code)      # 404
  print(e.error_messages)   # ['Issue does not exist or you do not have permission...']
  print(e.errors)           # {}
except RateLimitError as e:
  print(f'Retry after {e.retry_after} seconds')
except JiraError as e:
  print(f'Jira error: {e}')
```

| Exception             | HTTP Status | When                                  |
|-----------------------|-------------|---------------------------------------|
| `JiraError`           | any         | Base class for all Jira API errors    |
| `ValidationError`     | 400         | Bad request / invalid fields          |
| `AuthenticationError` | 401         | Invalid or missing credentials        |
| `ForbiddenError`      | 403         | Insufficient permissions              |
| `NotFoundError`       | 404         | Resource does not exist               |
| `RateLimitError`      | 429         | Too many requests (has `retry_after`) |
| `ServerError`         | 5xx         | Jira server error                     |

## Models

All responses are deserialized into [Pydantic v2](https://docs.pydantic.dev/latest/) models. Jira's camelCase JSON is mapped to snake_case Python attributes:

```python
issue = client.issues.get('PROJ-123')
issue.fields.fix_versions       # not fixVersions
issue.fields.status_category    # not statusCategory

user = client.users.myself()
user.display_name               # not displayName
user.email_address              # not emailAddress
```

Models use `extra='allow'`, so custom fields and unmodeled API fields are preserved:

```python
raw = issue.fields.model_extra
custom_value = raw.get('customfield_10042')
```

## Pagination

```python
# Manual
results = client.search.jql('project = PROJ', start_at=0, max_results=100)

# Auto-paginated (recommended)
for issue in client.search.jql_paginated('project = PROJ', page_size=100):
  process(issue)
```

The `Paginator` / `AsyncPaginator` classes can be used directly for any paginated endpoint:

```python
from pyjira.pagination import Paginator

def fetch_page(start_at, max_results):
  results = client.search.jql('...', start_at=start_at, max_results=max_results)
  return results.issues, results.total

for issue in Paginator(fetch_page, page_size=50):
  print(issue.key)
```

## Project Structure

```
src/pyjira/
  __init__.py          # Public API exports
  client.py            # JiraClient, AsyncJiraClient
  auth.py              # httpx.BasicAuth wrapper
  config.py            # JiraConfig dataclass
  exceptions.py        # Exception hierarchy + raise_for_response()
  pagination.py        # Paginator, AsyncPaginator
  models/              # Pydantic v2 models (23 files)
  resources/           # API resource classes (23 files, sync + async)
```

## Development

```bash
git clone https://github.com/faulander/pyjira.git
cd pyjira
uv sync --all-extras
uv run pytest -v
```

Tests use [respx](https://lundberg.github.io/respx/) to mock httpx requests. No real Jira instance is needed.

### Dependencies

**Runtime:** `httpx >= 0.28`, `pydantic >= 2.0`

**Dev:** `pytest >= 8.0`, `pytest-asyncio >= 0.24`, `respx >= 0.22`

## License

MIT
