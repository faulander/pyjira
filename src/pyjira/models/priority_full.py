from __future__ import annotations

from pydantic import Field

from pyjira.models.common import JiraModel, PaginatedResponse


class PriorityDetail(JiraModel):
    self_url: str | None = Field(None, alias="self")
    id: str | None = None
    name: str | None = None
    description: str | None = None
    icon_url: str | None = Field(None, alias="iconUrl")
    status_color: str | None = Field(None, alias="statusColor")
    is_default: bool | None = Field(None, alias="isDefault")


class PriorityPage(PaginatedResponse):
    values: list[PriorityDetail] = Field(default_factory=list)
