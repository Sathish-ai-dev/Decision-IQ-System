from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from app.shared.responses.base import GenericApiResponse


ItemT = TypeVar("ItemT")


class PaginationMeta(BaseModel):
    """Pagination metadata for list endpoints."""

    model_config = ConfigDict(extra="forbid")

    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    total_items: int = Field(ge=0)
    total_pages: int = Field(ge=0)
    has_next: bool = Field(default=False)
    has_previous: bool = Field(default=False)


class PaginationResponse(GenericApiResponse[list[ItemT], PaginationMeta], Generic[ItemT]):
    """Standard paginated response envelope."""

    model_config = ConfigDict(extra="forbid")

    success: bool = Field(default=True, frozen=True)
    message: str = Field(default="Items retrieved successfully.")
    data: list[ItemT] = Field(default_factory=list)
    meta: PaginationMeta = Field(...)
