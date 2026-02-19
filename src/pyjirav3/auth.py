from __future__ import annotations

import httpx


def build_auth(email: str, api_token: str) -> httpx.BasicAuth:
  """Build httpx BasicAuth from Jira credentials.

  Jira Cloud uses HTTP Basic auth with email as username
  and an API token (not password) as the password.
  """
  return httpx.BasicAuth(username=email, password=api_token)
