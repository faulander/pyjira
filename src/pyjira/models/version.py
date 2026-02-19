from __future__ import annotations

from typing import Any

from pydantic import Field

from pyjira.models.common import JiraModel


class Version(JiraModel):
    self_url: str | None = Field(None, alias="self")
    id: str | None = None
    name: str | None = None
    description: str | None = None
    archived: bool | None = None
    released: bool | None = None
    overdue: bool | None = None
    start_date: str | None = Field(None, alias="startDate")
    release_date: str | None = Field(None, alias="releaseDate")
    user_start_date: str | None = Field(None, alias="userStartDate")
    user_release_date: str | None = Field(None, alias="userReleaseDate")
    project_id: int | None = Field(None, alias="projectId")
    expand: str | None = None
