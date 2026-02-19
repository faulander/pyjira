from __future__ import annotations

from typing import Any

from pydantic import Field

from pyjira.models.common import JiraModel, PaginatedResponse
from pyjira.models.issue import StatusCategory


class StatusDetail(JiraModel):
    self_url: str | None = Field(None, alias="self")
    id: str | None = None
    name: str | None = None
    description: str | None = None
    icon_url: str | None = Field(None, alias="iconUrl")
    status_category: StatusCategory | None = Field(None, alias="statusCategory")
    scope: Any | None = None


class StatusPage(PaginatedResponse):
    values: list[StatusDetail] = Field(default_factory=list)
