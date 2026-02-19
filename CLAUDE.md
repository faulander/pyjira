# pyJira - CLAUDE.md

## Project Overview

Python client library for the Jira Cloud REST API v3. Provides both sync and async clients with fully-typed Pydantic models.

- **PyPI name:** `pyjirav3` (due to name clash, but import name is `pyjira`)
- **Import name:** `pyjira` (all internal imports use this)
- **Package source:** `src/pyjira/`

## Commands

```bash
uv run pytest -v          # Run all tests
uv run pytest -v -k test_get_issue  # Run specific test
uv pip install -e .       # Install in editable mode
```

## Architecture

### Project Structure

```
src/pyjira/
  __init__.py              # Public API exports
  client.py                # JiraClient (sync) + AsyncJiraClient (async)
  config.py                # JiraConfig dataclass
  auth.py                  # httpx BasicAuth builder
  exceptions.py            # Error hierarchy: JiraError -> AuthenticationError, NotFoundError, etc.
  pagination.py            # Paginator / AsyncPaginator iterators
  models/
    __init__.py            # Re-exports all models
    common.py              # JiraModel base, PaginatedResponse, AvatarUrls, EntityProperty
    errors.py              # ErrorResponse model
    issue.py               # Issue, IssueFields, Transition, Worklog, Votes, Watchers, Attachment, RemoteIssueLink, etc.
    project.py             # Project, ProjectCategory
    user.py                # User
    comment.py             # Comment, Visibility
    search.py              # SearchResults
  resources/
    __init__.py            # Re-exports all resource classes
    issues.py              # IssueResource + AsyncIssueResource
    projects.py            # ProjectResource + AsyncProjectResource
    users.py               # UserResource + AsyncUserResource
    search.py              # SearchResource + AsyncSearchResource
    comments.py            # CommentResource + AsyncCommentResource
tests/
  conftest.py              # Fixtures: mock_api (respx), client, shared JSON constants
  test_issues.py           # Issue CRUD + transition tests
  test_client.py           # Client init and context manager tests
  test_search.py           # JQL search tests
  test_pagination.py       # Paginator tests
docs/
  rest_api_v3_issues.json  # OpenAPI spec for Jira REST API v3 (reference for endpoints)
```

### How to Add a New Jira Endpoint Group

Follow these steps to add a new resource (e.g., boards, sprints, issue links):

#### 1. Add Models (`src/pyjira/models/`)

- Create a new file or add to an existing one (e.g., `models/issue.py` for issue-related sub-resources)
- Extend `JiraModel` for response models, `PaginatedResponse` for paginated responses
- Use `Field(None, alias='camelCase')` to map Jira's camelCase JSON to snake_case Python
- All fields should be `| None` with default `None` (Jira responses are sparse)
- Use `Any` for ADF document bodies and other complex untyped payloads

```python
from pyjira.models.common import JiraModel, PaginatedResponse

class MyModel(JiraModel):
  self_url: str | None = Field(None, alias='self')
  id: str | None = None
  display_name: str | None = Field(None, alias='displayName')

class MyModelPage(PaginatedResponse):
  values: list[MyModel] = Field(default_factory=list)
```

#### 2. Add Resource Classes (`src/pyjira/resources/`)

- Create a new file with both `FooResource` (sync) and `AsyncFooResource` (async)
- Constructor takes `httpx.Client` / `httpx.AsyncClient` (use `TYPE_CHECKING` guard)
- Every HTTP call must be followed by `raise_for_response(response)`
- Async methods are identical to sync but with `async def` + `await`
- Query params are built as `dict[str, str]`, only added when non-default
- Request bodies use `dict[str, Any]` for flexibility
- Return typed models via `Model.model_validate(response.json())`
- For list responses wrapped in a key, extract first: `data.get('values', [])`
- For `204 No Content` responses, return `None`

```python
from pyjira.exceptions import raise_for_response
from pyjira.models.foo import Foo

class FooResource:
  def __init__(self, client: httpx.Client) -> None:
    self._client = client

  def get(self, foo_id: str) -> Foo:
    response = self._client.get(f'/rest/api/3/foo/{foo_id}')
    raise_for_response(response)
    return Foo.model_validate(response.json())

class AsyncFooResource:
  def __init__(self, client: httpx.AsyncClient) -> None:
    self._client = client

  async def get(self, foo_id: str) -> Foo:
    response = await self._client.get(f'/rest/api/3/foo/{foo_id}')
    raise_for_response(response)
    return Foo.model_validate(response.json())
```

#### 3. Wire Into Client (`src/pyjira/client.py`)

- Import both sync and async resource classes
- Add `self.foos = FooResource(self._http)` in `JiraClient.__init__`
- Add `self.foos = AsyncFooResource(self._http)` in `AsyncJiraClient.__init__`

#### 4. Update Exports

- `models/__init__.py` - add model imports and `__all__` entries
- `resources/__init__.py` - add resource class imports and `__all__` entries
- `__init__.py` (top-level) - add key models to public API `__all__`

#### 5. Add Tests (`tests/`)

- Use `respx` to mock HTTP responses (see `conftest.py` for `mock_api` and `client` fixtures)
- Mock routes: `mock_api.get('/rest/api/3/...').mock(return_value=httpx.Response(200, json=...))`
- Test the sync client via the `client` fixture (from conftest)
- Add shared JSON fixtures to `conftest.py` if reused across test files
- Test both happy path and error cases (404, 401)

### Key Patterns

- **Dual sync/async:** Every resource has both sync and async variants with identical signatures
- **Error handling:** `raise_for_response()` maps HTTP status codes to typed exceptions (400->ValidationError, 401->AuthenticationError, 403->ForbiddenError, 404->NotFoundError, 429->RateLimitError, 5xx->ServerError)
- **All API paths** use `/rest/api/3/` prefix (Jira Cloud v3)
- **Multipart uploads** (attachments): use `files={'file': (name, bytes)}` with header `{'X-Atlassian-Token': 'no-check'}` and `content=None`
- **Base URL** is set on the httpx client, so resource methods use relative paths like `/rest/api/3/issue/{id}`
- **OpenAPI reference** is at `docs/rest_api_v3_issues.json` - use it to check endpoint signatures, query params, request/response schemas

### Code Style

- 2-space indentation
- Single quotes for strings
- snake_case for functions/variables, PascalCase for classes
- Type hints on all function signatures
- `from __future__ import annotations` in all modules
- `TYPE_CHECKING` guard for httpx imports in resource files
