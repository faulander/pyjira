from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from pyjira.models.common import JiraModel
from pyjira.models.project import Project
from pyjira.models.user import User


class StatusCategory(JiraModel):
  self_url: str | None = Field(None, alias='self')
  id: int | None = None
  key: str | None = None
  name: str | None = None
  color_name: str | None = Field(None, alias='colorName')


class Status(JiraModel):
  self_url: str | None = Field(None, alias='self')
  id: str | None = None
  name: str | None = None
  description: str | None = None
  icon_url: str | None = Field(None, alias='iconUrl')
  status_category: StatusCategory | None = Field(None, alias='statusCategory')


class Priority(JiraModel):
  self_url: str | None = Field(None, alias='self')
  id: str | None = None
  name: str | None = None
  icon_url: str | None = Field(None, alias='iconUrl')


class IssueType(JiraModel):
  self_url: str | None = Field(None, alias='self')
  id: str | None = None
  name: str | None = None
  description: str | None = None
  icon_url: str | None = Field(None, alias='iconUrl')
  subtask: bool | None = None
  avatar_id: int | None = Field(None, alias='avatarId')


class Resolution(JiraModel):
  self_url: str | None = Field(None, alias='self')
  id: str | None = None
  name: str | None = None
  description: str | None = None


class IssueFields(JiraModel):
  summary: str | None = None
  description: Any | None = None  # ADF document in v3
  status: Status | None = None
  priority: Priority | None = None
  issuetype: IssueType | None = None
  project: Project | None = None
  assignee: User | None = None
  reporter: User | None = None
  creator: User | None = None
  resolution: Resolution | None = None
  created: datetime | None = None
  updated: datetime | None = None
  resolution_date: datetime | None = Field(None, alias='resolutiondate')
  due_date: str | None = Field(None, alias='duedate')
  labels: list[str] | None = None
  components: list[Any] | None = None
  fix_versions: list[Any] | None = Field(None, alias='fixVersions')
  versions: list[Any] | None = None
  environment: Any | None = None
  parent: Issue | None = None
  subtasks: list[Issue] | None = None


class Transition(JiraModel):
  id: str | None = None
  name: str | None = None
  to: Status | None = None
  has_screen: bool | None = Field(None, alias='hasScreen')
  is_global: bool | None = Field(None, alias='isGlobal')
  is_initial: bool | None = Field(None, alias='isInitial')
  is_conditional: bool | None = Field(None, alias='isConditional')
  is_looped: bool | None = Field(None, alias='isLooped')


class Changelog(JiraModel):
  start_at: int | None = Field(None, alias='startAt')
  max_results: int | None = Field(None, alias='maxResults')
  total: int | None = None
  histories: list[ChangeHistory] | None = None


class ChangeHistory(JiraModel):
  id: str | None = None
  author: User | None = None
  created: datetime | None = None
  items: list[ChangeItem] | None = None


class ChangeItem(JiraModel):
  field: str | None = None
  fieldtype: str | None = None
  field_id: str | None = Field(None, alias='fieldId')
  from_value: str | None = Field(None, alias='from')
  from_string: str | None = Field(None, alias='fromString')
  to_value: str | None = Field(None, alias='to')
  to_string: str | None = Field(None, alias='toString')


class Issue(JiraModel):
  self_url: str | None = Field(None, alias='self')
  id: str | None = None
  key: str | None = None
  expand: str | None = None
  fields: IssueFields | None = None
  changelog: Changelog | None = None
  transitions: list[Transition] | None = None
  names: dict[str, str] | None = None


# Resolve forward references
IssueFields.model_rebuild()
Changelog.model_rebuild()
