# Error Handling

All Jira API errors raise typed exceptions with structured error data from the response.

## Basic Usage

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

## Exception Hierarchy

```
JiraError (base)
  +-- ValidationError      (400 Bad Request)
  +-- AuthenticationError  (401 Unauthorized)
  +-- ForbiddenError       (403 Forbidden)
  +-- NotFoundError        (404 Not Found)
  +-- RateLimitError       (429 Too Many Requests)
  +-- ServerError          (5xx Server Errors)
```

| Exception             | HTTP Status | When                                  |
|-----------------------|-------------|---------------------------------------|
| `JiraError`           | any         | Base class for all Jira API errors    |
| `ValidationError`     | 400         | Bad request / invalid fields          |
| `AuthenticationError` | 401         | Invalid or missing credentials        |
| `ForbiddenError`      | 403         | Insufficient permissions              |
| `NotFoundError`       | 404         | Resource does not exist               |
| `RateLimitError`      | 429         | Too many requests                     |
| `ServerError`         | 5xx         | Jira server error                     |

## Exception Attributes

Every exception carries these attributes:

| Attribute | Type | Description |
|-----------|------|-------------|
| `status_code` | `int \| None` | HTTP status code |
| `error_messages` | `list[str]` | Human-readable error messages from Jira |
| `errors` | `dict[str, str]` | Field-level errors (e.g. `{'summary': 'Field is required'}`) |
| `response` | `httpx.Response \| None` | Raw response for advanced inspection |

`RateLimitError` has one additional attribute:

| Attribute | Type | Description |
|-----------|------|-------------|
| `retry_after` | `int \| None` | Seconds to wait before retrying |

## Handling Rate Limits

```python
import time

def get_issue_with_retry(client, key, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.issues.get(key)
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            wait = e.retry_after or 10
            time.sleep(wait)
```

## Inspecting Raw Responses

For debugging, you can access the raw `httpx.Response` on any exception:

```python
try:
    client.issues.create(fields={})
except ValidationError as e:
    print(e.response.status_code)
    print(e.response.headers)
    print(e.response.text)
```
