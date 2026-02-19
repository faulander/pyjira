from __future__ import annotations

from pydantic import Field

from pyjira.models.common import AvatarUrls, JiraModel
from pyjira.models.user import User


class ProjectCategory(JiraModel):
  self_url: str | None = Field(None, alias='self')
  id: str | None = None
  name: str | None = None
  description: str | None = None


class Project(JiraModel):
  self_url: str | None = Field(None, alias='self')
  id: str | None = None
  key: str | None = None
  name: str | None = None
  description: str | None = None
  lead: User | None = None
  project_type_key: str | None = Field(None, alias='projectTypeKey')
  simplified: bool | None = None
  style: str | None = None
  is_private: bool | None = Field(None, alias='isPrivate')
  avatar_urls: AvatarUrls | None = Field(None, alias='avatarUrls')
  project_category: ProjectCategory | None = Field(None, alias='projectCategory')
