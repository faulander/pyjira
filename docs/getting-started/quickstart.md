# Quick Start

## Create a Client

```python
from pyjira import JiraClient

client = JiraClient(
    domain='mycompany',
    email='you@example.com',
    api_token='your-api-token',
)
```

This connects to `https://mycompany.atlassian.net`.

## Use as a Context Manager

The recommended pattern is to use the client as a context manager, which automatically closes the underlying HTTP connection pool:

```python
with JiraClient(domain='mycompany', email='you@example.com', api_token='tok') as client:
    issue = client.issues.get('PROJ-123')
    print(issue.key, issue.fields.summary)
```

## Fetch an Issue

```python
issue = client.issues.get('PROJ-123')

print(issue.key)                           # 'PROJ-123'
print(issue.fields.summary)                # 'Fix login bug'
print(issue.fields.status.name)            # 'In Progress'
print(issue.fields.assignee.display_name)  # 'Jane Doe'
```

## Search with JQL

```python
results = client.search.jql('project = PROJ AND status = "In Progress"')

for issue in results.issues:
    print(issue.key, issue.fields.summary)
```

## Auto-Paginated Search

Iterate through all results without managing pagination manually:

```python
for issue in client.search.jql_paginated('project = PROJ', page_size=100):
    print(issue.key)
```

## Create an Issue

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

:::{note}
Jira API v3 uses [Atlassian Document Format (ADF)](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/) for rich text fields like `description` and comment bodies.
:::

## Async Usage

Every sync method has an identical async counterpart:

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

## Next Steps

- {doc}`authentication` -- Learn about authentication options
- {doc}`/guide/issues` -- Full issue resource documentation
- {doc}`/guide/search` -- Advanced JQL search
- {doc}`/advanced/error-handling` -- Error handling patterns
