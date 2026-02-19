# pyJiraV3

A modern, fully-typed Python client for the [Jira Cloud REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/).

Built on [httpx](https://www.python-httpx.org/) and [Pydantic v2](https://docs.pydantic.dev/latest/). Supports both synchronous and asynchronous usage.

## Requirements

- Python 3.12+
- A Jira Cloud instance with an [API token](https://id.atlassian.com/manage/api-tokens)

## Installation

```bash
uv add pyjiraV3
```

Or install from source:

```bash
git clone https://github.com/faulander/pyJira.git
cd pyJira
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

The client exposes five resource attributes, each mapping to a Jira API group:

```python
client.issues     # Issue CRUD, transitions
client.projects   # Project listing and details
client.search     # JQL search with pagination
client.users      # User lookup
client.comments   # Issue comment CRUD
```

---

### Issues

#### Get an issue

```python
issue = client.issues.get('PROJ-123')

print(issue.key)                        # 'PROJ-123'
print(issue.fields.summary)             # 'Fix login bug'
print(issue.fields.status.name)         # 'In Progress'
print(issue.fields.assignee.display_name)  # 'Jane Doe'
print(issue.fields.priority.name)       # 'High'
print(issue.fields.labels)              # ['bug', 'auth']
```

Use `fields` to limit which fields are returned and `expand` to include additional data:

```python
issue = client.issues.get(
  'PROJ-123',
  fields=['summary', 'status', 'assignee'],
  expand=['changelog', 'transitions'],
)

# Access expanded data
for history in issue.changelog.histories:
  for item in history.items:
    print(f'{item.field}: {item.from_string} -> {item.to_string}')
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
  'priority': {'name': 'High'},
  'labels': ['bug', 'frontend'],
})

print(issue.key)  # 'PROJ-456'
```

> **Note:** Jira API v3 uses [Atlassian Document Format (ADF)](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/) for rich text fields like `description` and comment bodies.

#### Update an issue

```python
# Update via fields
client.issues.update('PROJ-123', fields={
  'summary': 'Updated summary',
  'priority': {'name': 'Critical'},
})

# Update via the update operation (for array fields like labels)
client.issues.update('PROJ-123', update={
  'labels': [{'add': 'urgent'}, {'remove': 'low-priority'}],
})

# Silently update (no email notifications)
client.issues.update('PROJ-123', fields={'summary': 'Quiet fix'}, notify_users=False)
```

#### Delete an issue

```python
client.issues.delete('PROJ-123')

# Also delete subtasks
client.issues.delete('PROJ-123', delete_subtasks=True)
```

#### Transitions

```python
# List available transitions
transitions = client.issues.get_transitions('PROJ-123')
for t in transitions:
  print(f'{t.id}: {t.name} -> {t.to.name}')

# Transition an issue (e.g. move to "In Progress")
client.issues.transition('PROJ-123', transition_id='31')

# Transition with a comment
client.issues.transition('PROJ-123', '31', comment={
  'type': 'doc',
  'version': 1,
  'content': [{
    'type': 'paragraph',
    'content': [{'type': 'text', 'text': 'Starting work on this.'}],
  }],
})
```

---

### Search (JQL)

#### Single-page search

```python
results = client.search.jql('project = PROJ AND status = "In Progress"')

print(results.total)       # 42
print(results.start_at)    # 0
print(results.max_results) # 50

for issue in results.issues:
  print(issue.key, issue.fields.summary)
```

Control pagination, fields, and expansion:

```python
results = client.search.jql(
  'assignee = currentUser() ORDER BY updated DESC',
  start_at=0,
  max_results=25,
  fields=['summary', 'status', 'updated'],
  expand=['changelog'],
)
```

#### Auto-paginated search

`jql_paginated` returns an iterator that transparently fetches pages as you consume results. No manual offset management needed:

```python
# Sync - iterates through ALL matching issues
for issue in client.search.jql_paginated('project = PROJ', page_size=100):
  print(issue.key)

# Collect into a list
all_issues = list(client.search.jql_paginated('project = PROJ'))
```

Async:

```python
async for issue in client.search.jql_paginated('project = PROJ'):
  print(issue.key)
```

---

### Projects

```python
# List all projects
projects = client.projects.list()
for p in projects:
  print(f'{p.key}: {p.name}')

# List with ordering
projects = client.projects.list(order_by='name')

# Get recently accessed projects
projects = client.projects.list(recent=5)

# Get a single project
project = client.projects.get('PROJ')
print(project.name)
print(project.lead.display_name)
print(project.project_type_key)  # 'software'
```

---

### Users

```python
# Get the authenticated user
me = client.users.myself()
print(me.display_name, me.email_address)

# Get a user by account ID
user = client.users.get('5b10ac8d82e05b22cc7d4ef5')
print(user.display_name)

# Search users
users = client.users.search(query='jane', max_results=10)
for u in users:
  print(u.display_name, u.account_id)
```

---

### Comments

```python
# List comments on an issue
page = client.comments.list('PROJ-123', max_results=20)
for comment in page.comments:
  print(f'{comment.author.display_name}: {comment.body}')
print(f'Showing {len(page.comments)} of {page.total}')

# Get a specific comment
comment = client.comments.get('PROJ-123', '10042')

# Add a comment (ADF body)
comment = client.comments.add('PROJ-123', body={
  'type': 'doc',
  'version': 1,
  'content': [{
    'type': 'paragraph',
    'content': [{'type': 'text', 'text': 'Looks good, merging now.'}],
  }],
})

# Add a restricted comment (visible only to a role)
comment = client.comments.add(
  'PROJ-123',
  body={'type': 'doc', 'version': 1, 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'Internal note.'}]}]},
  visibility={'type': 'role', 'value': 'Developers'},
)

# Update a comment
client.comments.update('PROJ-123', '10042', body={
  'type': 'doc',
  'version': 1,
  'content': [{
    'type': 'paragraph',
    'content': [{'type': 'text', 'text': 'Updated comment text.'}],
  }],
})

# Delete a comment
client.comments.delete('PROJ-123', '10042')
```

---

## Expand Parameter

The Jira API uses [resource expansion](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/#expansion) to keep responses compact. Pass `expand` as a list of strings to include additional data:

```python
# Expand changelog and transitions on an issue
issue = client.issues.get('PROJ-123', expand=['changelog', 'transitions'])

# Expand in search results
results = client.search.jql('project = PROJ', expand=['changelog', 'names'])
```

## Error Handling

All API errors raise typed exceptions with structured error data from the Jira response:

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
  print(e.error_messages)   # ['Issue does not exist or you do not have permission to see it.']
  print(e.errors)           # {}
  print(e.response)         # httpx.Response (for inspection)
except AuthenticationError:
  print('Check your email/token')
except RateLimitError as e:
  print(f'Rate limited. Retry after {e.retry_after} seconds')
except JiraError as e:
  print(f'Unexpected Jira error: {e}')
```

### Exception Hierarchy

| Exception             | HTTP Status | When                                  |
|-----------------------|-------------|---------------------------------------|
| `JiraError`           | any         | Base class for all Jira API errors    |
| `ValidationError`     | 400         | Bad request / invalid fields          |
| `AuthenticationError` | 401         | Invalid or missing credentials        |
| `ForbiddenError`      | 403         | Insufficient permissions              |
| `NotFoundError`       | 404         | Resource does not exist               |
| `RateLimitError`      | 429         | Too many requests (has `retry_after`) |
| `ServerError`         | 5xx         | Jira server error                     |

Every exception carries:
- `status_code: int | None` - HTTP status code
- `error_messages: list[str]` - Human-readable error messages from Jira
- `errors: dict[str, str]` - Field-level errors (e.g. `{'summary': 'Field is required'}`)
- `response: httpx.Response | None` - Raw response for advanced inspection

## Models

All API responses are deserialized into [Pydantic v2](https://docs.pydantic.dev/latest/) models with full type annotations. Models use `extra='allow'` so unknown fields from the API are preserved rather than dropped.

### Key Models

| Model          | Description                                     |
|----------------|-------------------------------------------------|
| `Issue`        | Jira issue with key, id, fields, changelog      |
| `IssueFields`  | Typed issue fields (summary, status, assignee..)|
| `Project`      | Project with key, name, lead, type              |
| `User`         | User with account_id, display_name, email       |
| `Comment`      | Issue comment with author, body, timestamps     |
| `SearchResults`| Paginated search response with issues list      |
| `Status`       | Issue status with category                      |
| `Priority`     | Issue priority                                  |
| `IssueType`    | Issue type (Bug, Task, Story...)                |
| `Transition`   | Workflow transition with target status           |
| `Resolution`   | Issue resolution (Fixed, Won't Fix...)          |
| `Changelog`    | Issue change history                            |
| `ChangeHistory`| Single changelog entry with author and items    |
| `ChangeItem`   | Individual field change (from -> to)            |

### Field Access

Jira's API returns camelCase JSON. Pydantic aliases map these to snake_case Python attributes:

```python
issue = client.issues.get('PROJ-123')

# Python attributes are snake_case
issue.fields.status_category    # not statusCategory
issue.fields.issue_type         # not issueType
issue.fields.fix_versions       # not fixVersions

user = client.users.myself()
user.display_name               # not displayName
user.email_address              # not emailAddress
user.account_id                 # not accountId
```

### Working with Raw Data

Since models use `extra='allow'`, any field the API returns that isn't explicitly modeled is still accessible:

```python
issue = client.issues.get('PROJ-123')

# Access custom fields or unmodeled fields via model_extra
raw = issue.fields.model_extra
custom_field_value = raw.get('customfield_10042')
```

## Pagination

The Jira API paginates large result sets using `startAt` / `maxResults` / `total`.

### Manual Pagination

```python
start = 0
page_size = 100
while True:
  results = client.search.jql('project = PROJ', start_at=start, max_results=page_size)
  for issue in results.issues:
    process(issue)
  start += len(results.issues)
  if start >= results.total:
    break
```

### Auto Pagination

The `jql_paginated` method handles this for you, yielding issues one at a time across pages:

```python
for issue in client.search.jql_paginated('project = PROJ', page_size=100):
  process(issue)
```

Under the hood, `Paginator` and `AsyncPaginator` are generic iterators you can use for any paginated operation:

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
  models/
    __init__.py        # Model re-exports
    common.py          # JiraModel base, AvatarUrls, PaginatedResponse
    errors.py          # ErrorResponse
    issue.py           # Issue, IssueFields, Status, Priority, Transition, Changelog...
    project.py         # Project, ProjectCategory
    user.py            # User
    comment.py         # Comment, Visibility
    search.py          # SearchResults
  resources/
    __init__.py        # Resource re-exports
    issues.py          # IssueResource, AsyncIssueResource
    projects.py        # ProjectResource, AsyncProjectResource
    search.py          # SearchResource, AsyncSearchResource
    users.py           # UserResource, AsyncUserResource
    comments.py        # CommentResource, AsyncCommentResource
```

## Development

### Setup

```bash
git clone https://github.com/faulander/pyJira.git
cd pyJira
uv sync --all-extras
```

### Run Tests

```bash
uv run pytest
uv run pytest -v          # verbose
uv run pytest -x          # stop on first failure
uv run pytest -k search   # run only search tests
```

Tests use [respx](https://lundberg.github.io/respx/) to mock httpx requests. No real Jira instance is needed.

### Dependencies

**Runtime:**
- `httpx >= 0.28` - HTTP client with sync and async support
- `pydantic >= 2.0` - Data validation and typed models

**Dev:**
- `pytest >= 8.0` - Test framework
- `pytest-asyncio >= 0.24` - Async test support
- `respx >= 0.22` - httpx request mocking

## License

MIT
