# pyJiraV3

A modern, fully-typed Python client for the [Jira Cloud REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/).

Built on [httpx](https://www.python-httpx.org/) and [Pydantic v2](https://docs.pydantic.dev/latest/). Supports both synchronous and asynchronous usage.

## Features

- **23 resource types** covering the full Jira Cloud REST API v3
- **Sync + async** -- every method works with both `httpx.Client` and `httpx.AsyncClient`
- **Fully typed** -- Pydantic v2 models with snake_case attributes and camelCase aliases
- **Auto-pagination** -- built-in `Paginator` / `AsyncPaginator` iterators
- **Typed exceptions** -- structured error hierarchy mapped from HTTP status codes
- **Extensible models** -- `extra='allow'` preserves unknown fields (custom fields, new API additions)

## Quick Example

```python
from pyjira import JiraClient

with JiraClient(domain='mycompany', email='you@example.com', api_token='tok') as client:
    issue = client.issues.get('PROJ-123')
    print(issue.key, issue.fields.summary)
```

```{toctree}
:maxdepth: 2
:caption: Getting Started

getting-started/installation
getting-started/quickstart
getting-started/authentication
```

```{toctree}
:maxdepth: 2
:caption: User Guide

guide/issues
guide/search
guide/projects
guide/users
guide/comments
guide/attachments
guide/components
guide/versions
guide/dashboards
guide/filters
guide/fields
guide/issue-links
guide/issue-types
guide/priorities
guide/resolutions
guide/statuses
guide/groups
guide/roles
guide/permissions
guide/workflows
guide/screens
guide/notification-schemes
guide/server-info
```

```{toctree}
:maxdepth: 2
:caption: Advanced

advanced/pagination
advanced/error-handling
advanced/models
advanced/async
```

```{toctree}
:maxdepth: 1
:caption: Development

development/contributing
development/changelog
```
