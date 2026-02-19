from __future__ import annotations

from typing import Any

from pydantic import Field

from pyjira.models.common import JiraModel, PaginatedResponse
from pyjira.models.user import User


class SharePermission(JiraModel):
    id: int | None = None
    type: str | None = None
    project: Any | None = None
    role: Any | None = None
    group: Any | None = None
    user: User | None = None


class Filter(JiraModel):
    self_url: str | None = Field(None, alias="self")
    id: str | None = None
    name: str | None = None
    description: str | None = None
    jql: str | None = None
    owner: User | None = None
    favourite: bool | None = None
    favourited_count: int | None = Field(None, alias="favouritedCount")
    share_permissions: list[SharePermission] | None = Field(
        None, alias="sharePermissions"
    )
    edit_permissions: list[SharePermission] | None = Field(
        None, alias="editPermissions"
    )
    search_url: str | None = Field(None, alias="searchUrl")
    view_url: str | None = Field(None, alias="viewUrl")


class FilterPage(PaginatedResponse):
    values: list[Filter] = Field(default_factory=list)
