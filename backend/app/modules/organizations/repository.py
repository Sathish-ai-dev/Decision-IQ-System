from __future__ import annotations

from collections.abc import Mapping
from math import ceil
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.organizations.models import Organization
from app.shared.responses.pagination import PaginationMeta


DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20
DEFAULT_SORT_BY = "created_at"
DEFAULT_SORT_ORDER = "desc"


class OrganizationRepository:
    """Persistence operations for organizations."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, organization: Organization) -> Organization:
        self.session.add(organization)
        self.session.flush()
        self.session.refresh(organization)
        return organization

    def get_by_id(self, organization_id: UUID) -> Organization | None:
        return self.session.get(Organization, organization_id)

    def get_by_slug(self, slug: str) -> Organization | None:
        statement = select(Organization).where(Organization.slug == slug)
        return self.session.scalar(statement)

    def list(
        self,
        *,
        page: int = DEFAULT_PAGE,
        page_size: int = DEFAULT_PAGE_SIZE,
        filters: Mapping[str, object] | None = None,
        sort_by: str = DEFAULT_SORT_BY,
        sort_order: str = DEFAULT_SORT_ORDER,
    ) -> tuple[list[Organization], PaginationMeta]:
        self._validate_pagination(page=page, page_size=page_size)
        conditions = self._build_conditions(filters)
        sort_column = self._resolve_sort_column(sort_by)
        order_expression = self._resolve_order_expression(sort_column, sort_order)

        total_items = self._count(conditions)
        total_pages = ceil(total_items / page_size) if total_items else 0
        offset = max(page - 1, 0) * page_size

        statement = (
            select(Organization)
            .where(*conditions)
            .order_by(order_expression)
            .offset(offset)
            .limit(page_size)
        )
        items = list(self.session.scalars(statement).all())
        meta = PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1 and total_pages > 0,
        )
        return items, meta

    def update(self, organization_id: UUID, **changes: object) -> Organization | None:
        organization = self.get_by_id(organization_id)
        if organization is None:
            return None

        for field, value in changes.items():
            if field not in self._updatable_fields():
                raise ValueError(f"Unsupported organization field: {field}")
            setattr(organization, field, value)

        self.session.flush()
        self.session.refresh(organization)
        return organization

    def delete(self, organization_id: UUID) -> bool:
        organization = self.get_by_id(organization_id)
        if organization is None:
            return False

        self.session.delete(organization)
        self.session.flush()
        return True

    def search(
        self,
        query: str,
        *,
        page: int = DEFAULT_PAGE,
        page_size: int = DEFAULT_PAGE_SIZE,
        filters: Mapping[str, object] | None = None,
        sort_by: str = DEFAULT_SORT_BY,
        sort_order: str = DEFAULT_SORT_ORDER,
    ) -> tuple[list[Organization], PaginationMeta]:
        self._validate_pagination(page=page, page_size=page_size)
        search_term = query.strip()
        if not search_term:
            return self.list(
                page=page,
                page_size=page_size,
                filters=filters,
                sort_by=sort_by,
                sort_order=sort_order,
            )

        conditions = self._build_conditions(filters)
        conditions.append(self._build_search_condition(search_term))

        sort_column = self._resolve_sort_column(sort_by)
        order_expression = self._resolve_order_expression(sort_column, sort_order)

        total_items = self._count(conditions)
        total_pages = ceil(total_items / page_size) if total_items else 0
        offset = max(page - 1, 0) * page_size

        statement = (
            select(Organization)
            .where(*conditions)
            .order_by(order_expression)
            .offset(offset)
            .limit(page_size)
        )
        items = list(self.session.scalars(statement).all())
        meta = PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1 and total_pages > 0,
        )
        return items, meta

    def _count(self, conditions: list[object]) -> int:
        statement = select(func.count()).select_from(Organization)
        if conditions:
            statement = statement.where(*conditions)
        return int(self.session.scalar(statement) or 0)

    @staticmethod
    def _validate_pagination(*, page: int, page_size: int) -> None:
        if page < 1:
            raise ValueError("page must be greater than or equal to 1.")
        if page_size < 1:
            raise ValueError("page_size must be greater than or equal to 1.")

    def _build_conditions(self, filters: Mapping[str, object] | None) -> list[object]:
        if not filters:
            return []

        conditions: list[object] = []
        for field, value in filters.items():
            if value is None:
                continue
            if field not in self._filterable_fields():
                raise ValueError(f"Unsupported organization filter: {field}")
            column = getattr(Organization, field)
            conditions.append(column == value)
        return conditions

    def _build_search_condition(self, query: str) -> object:
        pattern = f"%{query}%"
        return (
            Organization.name.ilike(pattern)
            | Organization.slug.ilike(pattern)
            | Organization.description.ilike(pattern)
            | Organization.website.ilike(pattern)
            | Organization.email.ilike(pattern)
            | Organization.phone.ilike(pattern)
            | Organization.address.ilike(pattern)
            | Organization.city.ilike(pattern)
            | Organization.state.ilike(pattern)
            | Organization.country.ilike(pattern)
            | Organization.postal_code.ilike(pattern)
            | Organization.organization_type.ilike(pattern)
        )

    def _resolve_sort_column(self, sort_by: str):
        if sort_by not in self._sortable_fields():
            raise ValueError(f"Unsupported organization sort field: {sort_by}")
        return getattr(Organization, sort_by)

    @staticmethod
    def _resolve_order_expression(column, sort_order: str):
        normalized = sort_order.strip().lower()
        if normalized == "asc":
            return column.asc()
        if normalized == "desc":
            return column.desc()
        raise ValueError("sort_order must be either 'asc' or 'desc'.")

    @staticmethod
    def _sortable_fields() -> set[str]:
        return set(Organization.__table__.columns.keys())

    @staticmethod
    def _filterable_fields() -> set[str]:
        return set(Organization.__table__.columns.keys())

    @staticmethod
    def _updatable_fields() -> set[str]:
        return {
            "address",
            "city",
            "country",
            "description",
            "email",
            "logo_url",
            "name",
            "organization_type",
            "owner_id",
            "phone",
            "postal_code",
            "slug",
            "state",
            "status",
            "website",
        }


__all__ = ["OrganizationRepository"]
