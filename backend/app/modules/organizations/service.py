from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import ValidationException
from app.models.user import User
from app.modules.organizations.models import Organization
from app.modules.organizations.repository import OrganizationRepository
from app.modules.organizations.schemas import (
    OrganizationCreate,
    OrganizationListResponse,
    OrganizationResponse,
    OrganizationSummary,
    OrganizationUpdate,
)


VALID_STATUSES = {"draft", "active", "archived", "processing", "failed"}


@dataclass(slots=True)
class OrganizationService:
    """Application-level organization workflows."""

    session: Session
    repository: OrganizationRepository | None = None

    def __post_init__(self) -> None:
        if self.repository is None:
            self.repository = OrganizationRepository(self.session)

    def create(self, payload: OrganizationCreate) -> OrganizationResponse:
        self._ensure_owner_exists(payload.owner_id)
        slug = self._normalize_slug(payload.slug)
        name = self._normalize_name(payload.name)
        status = self._normalize_status(payload.status)

        self._ensure_unique_slug(slug)
        self._ensure_unique_name(name)

        organization = Organization(
            name=name,
            slug=slug,
            description=payload.description.strip() if payload.description else None,
            logo_url=str(payload.logo_url) if payload.logo_url else None,
            website=str(payload.website) if payload.website else None,
            email=str(payload.email) if payload.email else None,
            phone=payload.phone.strip() if payload.phone else None,
            address=payload.address.strip() if payload.address else None,
            city=payload.city.strip() if payload.city else None,
            state=payload.state.strip() if payload.state else None,
            country=payload.country.strip() if payload.country else None,
            postal_code=payload.postal_code.strip() if payload.postal_code else None,
            organization_type=payload.organization_type.strip()
            if payload.organization_type
            else None,
            status=status,
            owner_id=payload.owner_id,
        )
        created = self.repository.create(organization)
        self.session.commit()
        return OrganizationResponse.model_validate(created)

    def get(self, organization_id: UUID) -> OrganizationResponse | None:
        organization = self.repository.get_by_id(organization_id)
        if organization is None:
            return None
        return OrganizationResponse.model_validate(organization)

    def get_by_slug(self, slug: str) -> OrganizationResponse | None:
        organization = self.repository.get_by_slug(self._normalize_slug(slug))
        if organization is None:
            return None
        return OrganizationResponse.model_validate(organization)

    def list(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        filters: dict[str, object] | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> OrganizationListResponse:
        items, meta = self.repository.list(
            page=page,
            page_size=page_size,
            filters=filters,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        return OrganizationListResponse(
            data=[OrganizationSummary.model_validate(item) for item in items],
            meta=meta,
        )

    def search(
        self,
        query: str,
        *,
        page: int = 1,
        page_size: int = 20,
        filters: dict[str, object] | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> OrganizationListResponse:
        items, meta = self.repository.search(
            query,
            page=page,
            page_size=page_size,
            filters=filters,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        return OrganizationListResponse(
            data=[OrganizationSummary.model_validate(item) for item in items],
            meta=meta,
        )

    def update(
        self,
        organization_id: UUID,
        payload: OrganizationUpdate,
    ) -> OrganizationResponse | None:
        organization = self.repository.get_by_id(organization_id)
        if organization is None:
            return None

        if payload.owner_id is not None:
            self._ensure_owner_exists(payload.owner_id)

        next_slug = (
            self._normalize_slug(payload.slug)
            if payload.slug is not None
            else organization.slug
        )
        next_name = (
            self._normalize_name(payload.name)
            if payload.name is not None
            else organization.name
        )
        next_status = (
            self._normalize_status(payload.status)
            if payload.status is not None
            else organization.status
        )

        if next_slug != organization.slug:
            self._ensure_unique_slug(next_slug, exclude_id=organization.id)
        if next_name != organization.name:
            self._ensure_unique_name(next_name, exclude_id=organization.id)

        changes: dict[str, object] = {}
        if "name" in payload.model_fields_set:
            changes["name"] = next_name
        if "slug" in payload.model_fields_set:
            changes["slug"] = next_slug
        if "description" in payload.model_fields_set:
            changes["description"] = self._normalize_optional_text(payload.description)
        if "logo_url" in payload.model_fields_set:
            changes["logo_url"] = str(payload.logo_url) if payload.logo_url else None
        if "website" in payload.model_fields_set:
            changes["website"] = str(payload.website) if payload.website else None
        if "email" in payload.model_fields_set:
            changes["email"] = str(payload.email) if payload.email else None
        if "phone" in payload.model_fields_set:
            changes["phone"] = self._normalize_optional_text(payload.phone)
        if "address" in payload.model_fields_set:
            changes["address"] = self._normalize_optional_text(payload.address)
        if "city" in payload.model_fields_set:
            changes["city"] = self._normalize_optional_text(payload.city)
        if "state" in payload.model_fields_set:
            changes["state"] = self._normalize_optional_text(payload.state)
        if "country" in payload.model_fields_set:
            changes["country"] = self._normalize_optional_text(payload.country)
        if "postal_code" in payload.model_fields_set:
            changes["postal_code"] = self._normalize_optional_text(payload.postal_code)
        if "organization_type" in payload.model_fields_set:
            changes["organization_type"] = self._normalize_optional_text(
                payload.organization_type
            )
        if "status" in payload.model_fields_set:
            changes["status"] = next_status
        if "owner_id" in payload.model_fields_set and payload.owner_id is not None:
            changes["owner_id"] = payload.owner_id

        updated = self.repository.update(organization_id, **changes)
        self.session.commit()
        return OrganizationResponse.model_validate(updated) if updated is not None else None

    def archive(self, organization_id: UUID) -> OrganizationResponse | None:
        organization = self.repository.get_by_id(organization_id)
        if organization is None:
            return None

        updated = self.repository.update(organization_id, status="archived")
        self.session.commit()
        return OrganizationResponse.model_validate(updated) if updated is not None else None

    def delete(self, organization_id: UUID) -> bool:
        deleted = self.repository.delete(organization_id)
        self.session.commit()
        return deleted

    def _ensure_owner_exists(self, owner_id: UUID) -> None:
        owner = self.session.get(User, owner_id)
        if owner is None or owner.deleted_at is not None:
            raise ValidationException("Owner account does not exist.")

    def _ensure_unique_slug(self, slug: str, *, exclude_id: UUID | None = None) -> None:
        organization = self.repository.get_by_slug(slug)
        if organization is not None and organization.id != exclude_id:
            raise ValidationException("An organization with this slug already exists.")

    def _ensure_unique_name(self, name: str, *, exclude_id: UUID | None = None) -> None:
        statement = select(Organization).where(func.lower(Organization.name) == name.lower())
        organization = self.session.scalar(statement)
        if organization is not None and organization.id != exclude_id:
            raise ValidationException("An organization with this name already exists.")

    def _normalize_status(self, status: str) -> str:
        normalized = status.strip().lower()
        if normalized not in VALID_STATUSES:
            raise ValidationException("Invalid organization status.")
        return normalized

    @staticmethod
    def _normalize_slug(slug: str) -> str:
        return slug.strip().lower()

    @staticmethod
    def _normalize_name(name: str) -> str:
        normalized = name.strip()
        if not normalized:
            raise ValidationException("Organization name cannot be empty.")
        return normalized

    @staticmethod
    def _normalize_optional_text(value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None


__all__ = ["OrganizationService", "VALID_STATUSES"]
