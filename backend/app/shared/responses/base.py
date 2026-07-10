from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field


DataT = TypeVar("DataT")
MetaT = TypeVar("MetaT")


class GenericApiResponse(BaseModel, Generic[DataT, MetaT]):
    """Generic API envelope for consistent JSON responses."""

    model_config = ConfigDict(extra="forbid")

    success: bool = Field(default=True)
    message: str = Field(default="Operation completed successfully.")
    data: DataT | None = Field(default=None)
    meta: MetaT | None = Field(default=None)


ApiResponse = GenericApiResponse

