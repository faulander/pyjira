from __future__ import annotations

from typing import Any

from pydantic import Field

from pyjira.models.common import JiraModel, PaginatedResponse


class NotificationScheme(JiraModel):
    self_url: str | None = Field(None, alias="self")
    id: int | None = None
    name: str | None = None
    description: str | None = None
    expand: str | None = None
    notification_scheme_events: list[Any] | None = Field(
        None, alias="notificationSchemeEvents"
    )
    scope: Any | None = None


class NotificationSchemePage(PaginatedResponse):
    values: list[NotificationScheme] = Field(default_factory=list)
