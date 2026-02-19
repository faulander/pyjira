from __future__ import annotations

from typing import Any

from pydantic import Field

from pyjira.models.common import JiraModel, PaginatedResponse


class WorkflowStatus(JiraModel):
    id: str | None = None
    name: str | None = None
    properties: Any | None = None


class Workflow(JiraModel):
    id: Any | None = None
    description: str | None = None
    is_default: bool | None = Field(None, alias="isDefault")
    has_draft_workflow: bool | None = Field(None, alias="hasDraftWorkflow")
    statuses: list[WorkflowStatus] | None = None
    transitions: list[Any] | None = None
    created: str | None = None
    updated: str | None = None


class WorkflowPage(PaginatedResponse):
    values: list[Workflow] = Field(default_factory=list)


class WorkflowScheme(JiraModel):
    self_url: str | None = Field(None, alias="self")
    id: int | None = None
    name: str | None = None
    description: str | None = None
    default_workflow: str | None = Field(None, alias="defaultWorkflow")
    issue_type_mappings: dict[str, str] | None = Field(None, alias="issueTypeMappings")
    draft: bool | None = None
    last_modified: str | None = Field(None, alias="lastModified")
    update_draft_if_needed: bool | None = Field(None, alias="updateDraftIfNeeded")
