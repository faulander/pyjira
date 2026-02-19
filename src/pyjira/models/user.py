from __future__ import annotations

from pydantic import Field

from pyjira.models.common import AvatarUrls, JiraModel


class User(JiraModel):
  self_url: str | None = Field(None, alias='self')
  account_id: str | None = Field(None, alias='accountId')
  email_address: str | None = Field(None, alias='emailAddress')
  display_name: str | None = Field(None, alias='displayName')
  active: bool | None = None
  time_zone: str | None = Field(None, alias='timeZone')
  locale: str | None = None
  avatar_urls: AvatarUrls | None = Field(None, alias='avatarUrls')
  account_type: str | None = Field(None, alias='accountType')
