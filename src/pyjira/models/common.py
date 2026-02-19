from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class JiraModel(BaseModel):
  """Base model for all Jira API responses."""

  model_config = ConfigDict(extra='allow', populate_by_name=True)


class AvatarUrls(JiraModel):
  url_16x16: str | None = Field(None, alias='16x16')
  url_24x24: str | None = Field(None, alias='24x24')
  url_32x32: str | None = Field(None, alias='32x32')
  url_48x48: str | None = Field(None, alias='48x48')


class EntityProperty(JiraModel):
  key: str | None = None
  value: Any | None = None


class PaginatedResponse(JiraModel):
  """Base for paginated API responses."""

  start_at: int = Field(0, alias='startAt')
  max_results: int = Field(0, alias='maxResults')
  total: int = 0
  is_last: bool | None = Field(None, alias='isLast')
