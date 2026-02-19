from __future__ import annotations

from typing import Any

from pydantic import Field

from pyjira.models.common import JiraModel, PaginatedResponse


class FieldDetail(JiraModel):
    id: str | None = None
    key: str | None = None
    name: str | None = None
    custom: bool | None = None
    orderable: bool | None = None
    navigable: bool | None = None
    searchable: bool | None = None
    clause_names: list[str] | None = Field(None, alias="clauseNames")
    schema: Any | None = None


class FieldPage(PaginatedResponse):
    values: list[FieldDetail] = Field(default_factory=list)
