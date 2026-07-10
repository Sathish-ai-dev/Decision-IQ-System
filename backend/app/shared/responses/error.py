from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ApiErrorResponse(BaseModel):
    """RFC 7807-inspired error detail for structured error reporting."""

    model_config = ConfigDict(extra="forbid")

    type: str = Field(default="about:blank")
    title: str = Field(default="Request failed.")
    status: int = Field(ge=100, le=599)
    detail: str | None = Field(default=None)
    instance: str | None = Field(default=None)
    errors: list[Any] | None = Field(default=None)


class StandardErrorResponse(BaseModel):
    """Standard error envelope for API responses."""

    model_config = ConfigDict(extra="forbid")

    success: bool = Field(default=False, frozen=True)
    message: str = Field(default="Request failed.")
    errors: list[ApiErrorResponse] = Field(default_factory=list)
    data: None = Field(default=None)
    meta: None = Field(default=None)
