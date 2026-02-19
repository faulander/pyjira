from __future__ import annotations

from typing import Any

from pydantic import Field

from pyjira.models.common import JiraModel, PaginatedResponse
from pyjira.models.user import User


class Dashboard(JiraModel):
    self_url: str | None = Field(None, alias="self")
    id: str | None = None
    name: str | None = None
    description: str | None = None
    owner: User | None = None
    is_favourite: bool | None = Field(None, alias="isFavourite")
    is_writable: bool | None = Field(None, alias="isWritable")
    popularity: int | None = None
    rank: int | None = None
    share_permissions: list[Any] | None = Field(None, alias="sharePermissions")
    edit_permissions: list[Any] | None = Field(None, alias="editPermissions")
    view: str | None = None
    system_dashboard: bool | None = Field(None, alias="systemDashboard")
    automatic_refresh_ms: int | None = Field(None, alias="automaticRefreshMs")


class DashboardPage(PaginatedResponse):
    dashboards: list[Dashboard] = Field(default_factory=list)


class DashboardGadget(JiraModel):
    id: int | None = None
    color: str | None = None
    module_key: str | None = Field(None, alias="moduleKey")
    position: Any | None = None
    title: str | None = None
    uri: str | None = None
