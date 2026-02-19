# Models

All API responses are deserialized into [Pydantic v2](https://docs.pydantic.dev/latest/) models with full type annotations.

## Base Classes

### JiraModel

All models inherit from `JiraModel`, which extends Pydantic's `BaseModel` with:

- **`extra='allow'`** -- unknown fields from the API are preserved in `model_extra`
- **`populate_by_name=True`** -- fields can be accessed by either their Python name or JSON alias

### PaginatedResponse

Base class for paginated API responses. Provides:

| Field | Type | Description |
|-------|------|-------------|
| `start_at` | `int` | Starting index (alias: `startAt`) |
| `max_results` | `int` | Page size (alias: `maxResults`) |
| `total` | `int` | Total number of results |
| `is_last` | `bool \| None` | Whether this is the last page (alias: `isLast`) |

## Field Naming

Jira's API returns camelCase JSON. Pydantic aliases map these to snake_case Python attributes:

```python
issue = client.issues.get('PROJ-123')

# Python attributes are snake_case
issue.fields.fix_versions       # not fixVersions
issue.fields.status_category    # not statusCategory

user = client.users.myself()
user.display_name               # not displayName
user.email_address              # not emailAddress
user.account_id                 # not accountId
```

## Accessing Custom Fields

Since models use `extra='allow'`, any field the API returns that isn't explicitly modeled is preserved:

```python
issue = client.issues.get('PROJ-123')

# Access custom fields via model_extra
raw = issue.fields.model_extra
custom_value = raw.get('customfield_10042')
```

## Core Models

### Issue Models

| Model | Description |
|-------|-------------|
| `Issue` | Complete issue with key, id, fields, changelog, transitions |
| `IssueFields` | All standard issue fields (summary, status, assignee, etc.) |
| `Status` | Issue status with category |
| `StatusCategory` | Status category (To Do, In Progress, Done) |
| `Priority` | Issue priority |
| `IssueType` | Issue type (Bug, Task, Story, etc.) |
| `Resolution` | Issue resolution (Fixed, Won't Fix, etc.) |
| `Transition` | Workflow transition with target status |
| `Changelog` | Issue change history container |
| `ChangeHistory` | Single changelog entry with author and items |
| `ChangeItem` | Individual field change (from -> to) |
| `Attachment` | Issue attachment with metadata |
| `Votes` | Issue voting information |
| `Watchers` | Issue watcher information |
| `Worklog` | Time tracking worklog entry |
| `RemoteIssueLink` | External issue link |
| `PropertyKey` | Entity property key reference |

### Project Models

| Model | Description |
|-------|-------------|
| `Project` | Project with key, name, lead, type, category |
| `ProjectCategory` | Project category metadata |

### User Models

| Model | Description |
|-------|-------------|
| `User` | User with account_id, display_name, email, avatar |
| `AvatarUrls` | Avatar URLs for different sizes (16x16 to 48x48) |

### Comment Models

| Model | Description |
|-------|-------------|
| `Comment` | Issue comment with author, body (ADF), timestamps |
| `Visibility` | Comment visibility restrictions |

### Search Models

| Model | Description |
|-------|-------------|
| `SearchResults` | Paginated search response with issues list |

### Issue Link Models

| Model | Description |
|-------|-------------|
| `IssueLink` | Link between two issues |
| `IssueLinkType` | Link type definition (inward/outward names) |
| `LinkedIssue` | Linked issue reference |

### Version Models

| Model | Description |
|-------|-------------|
| `Version` | Project version with release dates and status |

### Component Models

| Model | Description |
|-------|-------------|
| `Component` | Project component with lead and assignee |
| `ComponentIssueCount` | Component issue count |

### Filter Models

| Model | Description |
|-------|-------------|
| `Filter` | Saved JQL filter with owner and permissions |
| `FilterPage` | Paginated filter list |
| `SharePermission` | Filter share permission entry |

### Dashboard Models

| Model | Description |
|-------|-------------|
| `Dashboard` | Dashboard with owner and permissions |
| `DashboardPage` | Paginated dashboard list |
| `DashboardGadget` | Dashboard gadget/widget |

### Group Models

| Model | Description |
|-------|-------------|
| `Group` | User group |
| `GroupMembers` | Paginated group members list |

### Role Models

| Model | Description |
|-------|-------------|
| `ProjectRole` | Project role with actors |
| `RoleActor` | Role actor (user or group) |

### Permission Models

| Model | Description |
|-------|-------------|
| `PermissionScheme` | Permission scheme configuration |
| `PermissionGrant` | Permission grant entry |

### Priority / Resolution / Status Detail Models

| Model | Description |
|-------|-------------|
| `PriorityDetail` | Detailed priority with status color and default flag |
| `PriorityPage` | Paginated priority list |
| `ResolutionDetail` | Detailed resolution with default flag |
| `ResolutionPage` | Paginated resolution list |
| `StatusDetail` | Detailed status with icon and scope |
| `StatusPage` | Paginated status list |

### Field Models

| Model | Description |
|-------|-------------|
| `FieldDetail` | Field configuration (custom, orderable, searchable, etc.) |
| `FieldPage` | Paginated field list |
| `IssueTypeDetail` | Detailed issue type with hierarchy level and scope |

### Workflow Models

| Model | Description |
|-------|-------------|
| `Workflow` | Workflow definition with statuses and transitions |
| `WorkflowPage` | Paginated workflow list |
| `WorkflowScheme` | Workflow scheme configuration |
| `WorkflowStatus` | Status within a workflow |

### Screen Models

| Model | Description |
|-------|-------------|
| `Screen` | Screen definition |
| `ScreenPage` | Paginated screen list |
| `ScreenTab` | Screen tab |
| `ScreenField` | Field on a screen tab |
| `ScreenScheme` | Screen scheme configuration |
| `ScreenSchemePage` | Paginated screen scheme list |

### Notification Scheme Models

| Model | Description |
|-------|-------------|
| `NotificationScheme` | Notification scheme configuration |
| `NotificationSchemePage` | Paginated notification scheme list |
