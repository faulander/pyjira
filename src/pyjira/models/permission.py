from __future__ import annotations

from typing import Any

from pydantic import Field

from pyjira.models.common import JiraModel


class PermissionGrant(JiraModel):
    id: int | None = None
    self_url: str | None = Field(None, alias="self")
    holder: Any | None = None
    permission: str | None = None


class PermissionScheme(JiraModel):
    self_url: str | None = Field(None, alias="self")
    id: int | None = None
    name: str | None = None
    description: str | None = None
    permissions: list[PermissionGrant] | None = None
    expand: str | None = None
