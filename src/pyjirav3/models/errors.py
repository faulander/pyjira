from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ErrorResponse(BaseModel):
  model_config = ConfigDict(extra='allow')

  error_messages: list[str] | None = Field(None, alias='errorMessages')
  errors: dict[str, str] | None = None
  status: int | None = None
