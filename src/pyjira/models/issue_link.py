from __future__ import annotations

from typing import Any

from pydantic import Field

from pyjira.models.common import JiraModel


class IssueLinkType(JiraModel):
    self_url: str | None = Field(None, alias="self")
    id: str | None = None
    name: str | None = None
    inward: str | None = None
    outward: str | None = None


class LinkedIssue(JiraModel):
    self_url: str | None = Field(None, alias="self")
    id: str | None = None
    key: str | None = None
    fields: Any | None = None


class IssueLink(JiraModel):
    self_url: str | None = Field(None, alias="self")
    id: str | None = None
    type: IssueLinkType | None = None
    inward_issue: LinkedIssue | None = Field(None, alias="inwardIssue")
    outward_issue: LinkedIssue | None = Field(None, alias="outwardIssue")
