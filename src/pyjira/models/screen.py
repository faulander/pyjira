from __future__ import annotations

from typing import Any

from pydantic import Field

from pyjira.models.common import JiraModel, PaginatedResponse


class Screen(JiraModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    scope: Any | None = None


class ScreenPage(PaginatedResponse):
    values: list[Screen] = Field(default_factory=list)


class ScreenTab(JiraModel):
    id: int | None = None
    name: str | None = None


class ScreenField(JiraModel):
    id: str | None = None
    name: str | None = None


class ScreenScheme(JiraModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None


class ScreenSchemePage(PaginatedResponse):
    values: list[ScreenScheme] = Field(default_factory=list)
