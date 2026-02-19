# Changelog

## 0.1.2 (Current)

- Added 18 new resource types: attachments, components, dashboards, fields, filters, groups, issue links, issue types, notification schemes, permissions, priorities, resolutions, roles, screens, server info, statuses, versions, workflows
- Extended issue resource with 30+ methods (attachments, worklogs, watchers, votes, remote links, properties, changelogs)
- Added corresponding Pydantic v2 models for all new resources
- Total: 23 resource types covering the Jira Cloud REST API v3

## 0.1.1

- Added comment resource
- Improved error handling

## 0.1.0

- Initial release
- Core resources: issues, projects, search, users
- Sync and async client support
- Pydantic v2 models
- Auto-pagination
- Typed exception hierarchy
