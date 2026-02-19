from __future__ import annotations

from pydantic import Field

from pyjira.models.common import JiraModel, PaginatedResponse


class ResolutionDetail(JiraModel):
    self_url: str | None = Field(None, alias="self")
    id: str | None = None
    name: str | None = None
    description: str | None = None
    is_default: bool | None = Field(None, alias="isDefault")


class ResolutionPage(PaginatedResponse):
    values: list[ResolutionDetail] = Field(default_factory=list)
