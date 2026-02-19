from __future__ import annotations

from typing import Any

import httpx

from pyjira.models.errors import ErrorResponse


class JiraError(Exception):
  """Base exception for Jira API errors."""

  def __init__(
    self,
    message: str,
    *,
    status_code: int | None = None,
    error_messages: list[str] | None = None,
    errors: dict[str, str] | None = None,
    response: httpx.Response | None = None,
  ) -> None:
    super().__init__(message)
    self.status_code = status_code
    self.error_messages = error_messages or []
    self.errors = errors or {}
    self.response = response


class AuthenticationError(JiraError):
  """Raised on 401 Unauthorized."""


class ForbiddenError(JiraError):
  """Raised on 403 Forbidden."""


class NotFoundError(JiraError):
  """Raised on 404 Not Found."""


class ValidationError(JiraError):
  """Raised on 400 Bad Request."""


class RateLimitError(JiraError):
  """Raised on 429 Too Many Requests."""

  def __init__(
    self,
    message: str,
    *,
    retry_after: int | None = None,
    **kwargs: Any,
  ) -> None:
    super().__init__(message, **kwargs)
    self.retry_after = retry_after


class ServerError(JiraError):
  """Raised on 5xx Server Error."""


_STATUS_MAP: dict[int, type[JiraError]] = {
  400: ValidationError,
  401: AuthenticationError,
  403: ForbiddenError,
  404: NotFoundError,
  429: RateLimitError,
}


def raise_for_response(response: httpx.Response) -> None:
  """Raise a typed JiraError if the response indicates an error."""
  if response.is_success:
    return

  status_code = response.status_code
  error_messages: list[str] = []
  errors: dict[str, str] = {}
  message = f'Jira API error ({status_code})'

  try:
    data = response.json()
    error_resp = ErrorResponse.model_validate(data)
    error_messages = error_resp.error_messages or []
    errors = error_resp.errors or {}
    if error_messages:
      message = '; '.join(error_messages)
    elif errors:
      message = '; '.join(f'{k}: {v}' for k, v in errors.items())
  except Exception:
    message = f'Jira API error ({status_code}): {response.text[:200]}'

  kwargs: dict[str, Any] = {
    'status_code': status_code,
    'error_messages': error_messages,
    'errors': errors,
    'response': response,
  }

  if status_code == 429:
    retry_after_header = response.headers.get('Retry-After')
    retry_after = int(retry_after_header) if retry_after_header else None
    raise RateLimitError(message, retry_after=retry_after, **kwargs)

  if status_code >= 500:
    raise ServerError(message, **kwargs)

  exc_class = _STATUS_MAP.get(status_code, JiraError)
  raise exc_class(message, **kwargs)
