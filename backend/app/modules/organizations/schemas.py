from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl

from app.shared.responses.pagination import PaginationResponse


SLUG_PATTERN = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"


class OrganizationBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=1, max_length=255, pattern=SLUG_PATTERN)
    description: str | None = Field(default=None, max_length=1024)
    logo_url: HttpUrl | None = None
    website: HttpUrl | None = None
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=64)
    address: str | None = Field(default=None, max_length=1024)
    city: str | None = Field(default=None, max_length=128)
    state: str | None = Field(default=None, max_length=128)
    country: str | None = Field(default=None, max_length=128)
    postal_code: str | None = Field(default=None, max_length=32)
    organization_type: str | None = Field(default=None, max_length=64)
    status: str = Field(default="active", max_length=32)
    owner_id: UUID | None = None


class OrganizationCreate(OrganizationBase):
    """Payload for creating an organization."""

    owner_id: UUID


class OrganizationUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=255)
    slug: str | None = Field(default=None, min_length=1, max_length=255, pattern=SLUG_PATTERN)
    description: str | None = Field(default=None, max_length=1024)
    logo_url: HttpUrl | None = None
    website: HttpUrl | None = None
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=64)
    address: str | None = Field(default=None, max_length=1024)
    city: str | None = Field(default=None, max_length=128)
    state: str | None = Field(default=None, max_length=128)
    country: str | None = Field(default=None, max_length=128)
    postal_code: str | None = Field(default=None, max_length=32)
    organization_type: str | None = Field(default=None, max_length=64)
    status: str | None = Field(default=None, max_length=32)
    owner_id: UUID | None = None


class OrganizationSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: UUID
    name: str
    slug: str
    description: str | None = None
    logo_url: HttpUrl | None = None
    status: str
    created_at: datetime


class OrganizationResponse(OrganizationSummary):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    website: HttpUrl | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None
    organization_type: str | None = None
    owner_id: UUID
    updated_at: datetime
    deleted_at: datetime | None = None


class OrganizationListResponse(PaginationResponse[OrganizationSummary]):
    """Paginated organization list response."""


__all__ = [
    "OrganizationCreate",
    "OrganizationListResponse",
    "OrganizationResponse",
    "OrganizationSummary",
    "OrganizationUpdate",
]
