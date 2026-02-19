from __future__ import annotations

from typing import Any

from pydantic import Field

from pyjira.models.common import JiraModel, PaginatedResponse
from pyjira.models.user import User


class Group(JiraModel):
    name: str | None = None
    group_id: str | None = Field(None, alias="groupId")
    self_url: str | None = Field(None, alias="self")


class GroupMembers(PaginatedResponse):
    values: list[User] = Field(default_factory=list)
