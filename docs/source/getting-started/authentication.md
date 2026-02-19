# Authentication

pyJiraV3 uses Jira Cloud's [Basic auth with API tokens](https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/).

## Generate an API Token

1. Go to [https://id.atlassian.com/manage/api-tokens](https://id.atlassian.com/manage/api-tokens)
2. Click **Create API token**
3. Give it a label and click **Create**
4. Copy the token value

## Connect by Domain

If your Jira instance is at `https://mycompany.atlassian.net`:

```python
from pyjira import JiraClient

client = JiraClient(
    domain='mycompany',
    email='you@example.com',
    api_token='your-api-token',
)
```

## Connect by Base URL

For custom domains or on-premise proxies:

```python
client = JiraClient(
    base_url='https://jira.internal.company.com',
    email='you@example.com',
    api_token='your-api-token',
)
```

You must provide either `domain` or `base_url`, not both.

## Client Options

| Parameter   | Type              | Default | Description                                |
|-------------|-------------------|---------|--------------------------------------------|
| `domain`    | `str \| None`     | `None`  | Atlassian domain (e.g. `'mycompany'`)      |
| `base_url`  | `str \| None`     | `None`  | Full base URL (alternative to `domain`)    |
| `email`     | `str`             | --      | Atlassian account email                    |
| `api_token` | `str`             | --      | API token from Atlassian account settings  |
| `timeout`   | `float`           | `30.0`  | Request timeout in seconds                 |
| `headers`   | `dict \| None`    | `None`  | Additional HTTP headers to merge in        |

## Environment Variables

A common pattern is to load credentials from environment variables:

```python
import os
from pyjira import JiraClient

client = JiraClient(
    domain=os.environ['JIRA_DOMAIN'],
    email=os.environ['JIRA_EMAIL'],
    api_token=os.environ['JIRA_API_TOKEN'],
)
```

## Connection Lifecycle

Always close the client when done to release the HTTP connection pool:

```python
# Option 1: Context manager (recommended)
with JiraClient(domain='mycompany', email='...', api_token='...') as client:
    ...

# Option 2: Explicit close
client = JiraClient(domain='mycompany', email='...', api_token='...')
try:
    ...
finally:
    client.close()
```

The same applies to `AsyncJiraClient`:

```python
async with AsyncJiraClient(domain='mycompany', email='...', api_token='...') as client:
    ...
```
