from __future__ import annotations

from pydantic import Field

from pyjira.models.common import PaginatedResponse
from pyjira.models.issue import Issue


class SearchResults(PaginatedResponse):
  issues: list[Issue] = Field(default_factory=list)
  warning_messages: list[str] | None = Field(None, alias='warningMessages')
  names: dict[str, str] | None = None
  schema_map: dict[str, object] | None = Field(None, alias='schema')
  expand: str | None = None
