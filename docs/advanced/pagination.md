# Pagination

The Jira API paginates large result sets using `startAt` / `maxResults` / `total`.

## Manual Pagination

Control the pagination yourself by specifying `start_at` and `max_results`:

```python
start = 0
page_size = 100

while True:
    results = client.search.jql(
        'project = PROJ',
        start_at=start,
        max_results=page_size,
    )

    for issue in results.issues:
        process(issue)

    start += len(results.issues)
    if start >= results.total:
        break
```

## Auto-Pagination

The `jql_paginated` method returns an iterator that transparently fetches pages as you consume results:

```python
# Sync
for issue in client.search.jql_paginated('project = PROJ', page_size=100):
    print(issue.key)

# Collect all into a list
all_issues = list(client.search.jql_paginated('project = PROJ'))
```

### Async

```python
async for issue in client.search.jql_paginated('project = PROJ'):
    print(issue.key)
```

## Using Paginator Directly

The `Paginator` and `AsyncPaginator` classes are generic iterators you can use for any paginated operation:

```python
from pyjira.pagination import Paginator

def fetch_page(start_at, max_results):
    results = client.search.jql('...', start_at=start_at, max_results=max_results)
    return results.issues, results.total

for issue in Paginator(fetch_page, page_size=50):
    print(issue.key)
```

### AsyncPaginator

```python
from pyjira.pagination import AsyncPaginator

async def fetch_page(start_at, max_results):
    results = await client.search.jql('...', start_at=start_at, max_results=max_results)
    return results.issues, results.total

async for issue in AsyncPaginator(fetch_page, page_size=50):
    print(issue.key)
```

## Paginator API

### `Paginator[T]`

A synchronous iterator that auto-paginates through results.

**Constructor:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fetch_page` | `Callable[[int, int], tuple[list[T], int]]` | -- | Function that takes `(start_at, max_results)` and returns `(items, total)` |
| `page_size` | `int` | `50` | Number of items per page |

**Usage:** Implements `__iter__` and `__next__`. Raises `StopIteration` when all items have been yielded.

### `AsyncPaginator[T]`

An asynchronous iterator with the same interface.

**Constructor:** Same as `Paginator`, but `fetch_page` should be an async function.

**Usage:** Implements `__aiter__` and `__anext__`. Raises `StopAsyncIteration` when exhausted.
