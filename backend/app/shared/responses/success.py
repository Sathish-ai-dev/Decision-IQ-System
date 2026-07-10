from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import ConfigDict, Field

from app.shared.responses.base import GenericApiResponse


DataT = TypeVar("DataT")
MetaT = TypeVar("MetaT")


class StandardSuccessResponse(GenericApiResponse[DataT, MetaT], Generic[DataT, MetaT]):
    """Standard success response envelope."""

    model_config = ConfigDict(extra="forbid")

    success: bool = Field(default=True, frozen=True)
    message: str = Field(default="Operation completed successfully.")
