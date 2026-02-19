from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from pyjira.models.common import JiraModel
from pyjira.models.user import User


class Visibility(JiraModel):
  type: str | None = None
  value: str | None = None
  identifier: str | None = None


class Comment(JiraModel):
  self_url: str | None = Field(None, alias='self')
  id: str | None = None
  author: User | None = None
  update_author: User | None = Field(None, alias='updateAuthor')
  body: Any | None = None  # ADF document in v3
  created: datetime | None = None
  updated: datetime | None = None
  visibility: Visibility | None = None
  jsd_public: bool | None = Field(None, alias='jsdPublic')
