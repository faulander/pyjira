from __future__ import annotations

from typing import Any

from pydantic import Field

from pyjira.models.common import JiraModel
from pyjira.models.user import User


class Component(JiraModel):
    self_url: str | None = Field(None, alias="self")
    id: str | None = None
    name: str | None = None
    description: str | None = None
    lead: User | None = None
    lead_account_id: str | None = Field(None, alias="leadAccountId")
    assignee_type: str | None = Field(None, alias="assigneeType")
    assignee: User | None = None
    real_assignee_type: str | None = Field(None, alias="realAssigneeType")
    real_assignee: User | None = None
    is_assignee_type_valid: bool | None = Field(None, alias="isAssigneeTypeValid")
    project: str | None = None
    project_id: int | None = Field(None, alias="projectId")


class ComponentIssueCount(JiraModel):
    self_url: str | None = Field(None, alias="self")
    issue_count: int | None = Field(None, alias="issueCount")
