from __future__ import annotations

from typing import Any

from pydantic import Field

from pyjira.models.common import JiraModel


class RoleActor(JiraModel):
    id: int | None = None
    display_name: str | None = Field(None, alias="displayName")
    type: str | None = None
    name: str | None = None
    avatar_url: str | None = Field(None, alias="avatarUrl")
    actor_user: Any | None = Field(None, alias="actorUser")
    actor_group: Any | None = Field(None, alias="actorGroup")


class ProjectRole(JiraModel):
    self_url: str | None = Field(None, alias="self")
    id: int | None = None
    name: str | None = None
    description: str | None = None
    actors: list[RoleActor] | None = None
    admin: bool | None = None
    default: bool | None = None
    role_configurable: bool | None = Field(None, alias="roleConfigurable")
