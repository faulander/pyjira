# Async Usage

Every resource method in pyJiraV3 has both a synchronous and an asynchronous version with identical signatures.

## AsyncJiraClient

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

## Context Manager

Always use `async with` to ensure the connection pool is properly closed:

```python
async with AsyncJiraClient(domain='mycompany', email='...', api_token='...') as client:
    ...
```

Or close explicitly:

```python
client = AsyncJiraClient(domain='mycompany', email='...', api_token='...')
try:
    ...
finally:
    await client.close()
```

## Concurrent Requests

Async is particularly useful for making multiple API calls concurrently:

```python
import asyncio
from pyjira import AsyncJiraClient

async def main():
    async with AsyncJiraClient(domain='mycompany', email='...', api_token='...') as client:
        # Fetch multiple issues concurrently
        tasks = [
            client.issues.get('PROJ-1'),
            client.issues.get('PROJ-2'),
            client.issues.get('PROJ-3'),
        ]
        issues = await asyncio.gather(*tasks)

        for issue in issues:
            print(issue.key, issue.fields.summary)

asyncio.run(main())
```

## Async Pagination

The auto-paginator works with `async for`:

```python
async with AsyncJiraClient(domain='mycompany', email='...', api_token='...') as client:
    async for issue in client.search.jql_paginated('project = PROJ'):
        print(issue.key)
```

## Resource Parity

Every resource on `JiraClient` has an async counterpart on `AsyncJiraClient`. The attribute names are identical:

| Sync | Async |
|------|-------|
| `client.issues.get(...)` | `await client.issues.get(...)` |
| `client.search.jql(...)` | `await client.search.jql(...)` |
| `client.projects.list()` | `await client.projects.list()` |
| `for x in client.search.jql_paginated(...)` | `async for x in client.search.jql_paginated(...)` |

All 23 resources work identically in both sync and async modes.
