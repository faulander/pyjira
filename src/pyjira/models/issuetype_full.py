from __future__ import annotations

from typing import Any

from pydantic import Field

from pyjira.models.common import JiraModel


class IssueTypeDetail(JiraModel):
    self_url: str | None = Field(None, alias="self")
    id: str | None = None
    name: str | None = None
    description: str | None = None
    icon_url: str | None = Field(None, alias="iconUrl")
    subtask: bool | None = None
    avatar_id: int | None = Field(None, alias="avatarId")
    entity_id: str | None = Field(None, alias="entityId")
    hierarchy_level: int | None = Field(None, alias="hierarchyLevel")
    scope: Any | None = None
