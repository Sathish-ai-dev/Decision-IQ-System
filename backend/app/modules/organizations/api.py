from __future__ import annotations

from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.authorization import require_roles
from app.models.role import RoleName
from app.modules.organizations.repository import OrganizationRepository
from app.modules.organizations.schemas import (
    OrganizationCreate,
    OrganizationListResponse,
    OrganizationResponse,
    OrganizationUpdate,
)
from app.modules.organizations.service import OrganizationService
from app.services.auth_service import AuthenticatedUser


router = APIRouter(prefix="/organizations", tags=["Organizations"])

SortOrder = Literal["asc", "desc"]
OrganizationSortField = Literal[
    "address",
    "city",
    "country",
    "created_at",
    "deleted_at",
    "description",
    "email",
    "id",
    "logo_url",
    "name",
    "organization_type",
    "owner_id",
    "phone",
    "postal_code",
    "slug",
    "state",
    "status",
    "updated_at",
    "website",
]


def get_organization_service(db: Annotated[Session, Depends(get_db)]) -> OrganizationService:
    return OrganizationService(db, repository=OrganizationRepository(db))


def _build_filters(
    *,
    name: str | None = None,
    slug: str | None = None,
    status: str | None = None,
    owner_id: UUID | None = None,
    city: str | None = None,
    country: str | None = None,
    organization_type: str | None = None,
    email: str | None = None,
) -> dict[str, object]:
    filters: dict[str, object] = {}
    if name is not None:
        filters["name"] = name
    if slug is not None:
        filters["slug"] = slug
    if status is not None:
        filters["status"] = status
    if owner_id is not None:
        filters["owner_id"] = owner_id
    if city is not None:
        filters["city"] = city
    if country is not None:
        filters["country"] = country
    if organization_type is not None:
        filters["organization_type"] = organization_type
    if email is not None:
        filters["email"] = email
    return filters


ReadOrganization = Annotated[
    AuthenticatedUser,
    Depends(
        require_roles(
            RoleName.ADMIN,
            RoleName.ANALYST,
            RoleName.ORGANIZATION,
            RoleName.COMMUNITY,
            RoleName.CITIZEN,
        )
    ),
]

ManageOrganization = Annotated[
    AuthenticatedUser,
    Depends(require_roles(RoleName.ADMIN, RoleName.ORGANIZATION)),
]


@router.get(
    "",
    response_model=OrganizationListResponse,
    summary="List organizations",
    description="Return a paginated, filtered, and sortable list of organizations.",
)
def list_organizations(
    service: Annotated[OrganizationService, Depends(get_organization_service)],
    _user: ReadOrganization,
    page: Annotated[int, Query(ge=1, description="Page number starting at 1.")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page.")] = 20,
    sort_by: Annotated[
        OrganizationSortField,
        Query(description="Column used to sort results."),
    ] = "created_at",
    sort_order: Annotated[SortOrder, Query(description="Sort direction.")] = "desc",
    name: Annotated[str | None, Query(description="Filter by exact organization name.")] = None,
    slug: Annotated[str | None, Query(description="Filter by exact organization slug.")] = None,
    status: Annotated[str | None, Query(description="Filter by organization status.")] = None,
    owner_id: Annotated[UUID | None, Query(description="Filter by owner UUID.")] = None,
    city: Annotated[str | None, Query(description="Filter by city.")] = None,
    country: Annotated[str | None, Query(description="Filter by country.")] = None,
    organization_type: Annotated[
        str | None,
        Query(description="Filter by organization type."),
    ] = None,
    email: Annotated[str | None, Query(description="Filter by contact email.")] = None,
) -> OrganizationListResponse:
    filters = _build_filters(
        name=name,
        slug=slug,
        status=status,
        owner_id=owner_id,
        city=city,
        country=country,
        organization_type=organization_type,
        email=email,
    )
    return service.list(
        page=page,
        page_size=page_size,
        filters=filters or None,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get(
    "/search",
    response_model=OrganizationListResponse,
    summary="Search organizations",
    description="Search organizations by text while still supporting filters, sorting, and pagination.",
)
def search_organizations(
    q: Annotated[str, Query(min_length=1, description="Search text.")],
    service: Annotated[OrganizationService, Depends(get_organization_service)],
    _user: ReadOrganization,
    page: Annotated[int, Query(ge=1, description="Page number starting at 1.")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page.")] = 20,
    sort_by: Annotated[
        OrganizationSortField,
        Query(description="Column used to sort results."),
    ] = "created_at",
    sort_order: Annotated[SortOrder, Query(description="Sort direction.")] = "desc",
    name: Annotated[str | None, Query(description="Filter by exact organization name.")] = None,
    slug: Annotated[str | None, Query(description="Filter by exact organization slug.")] = None,
    status: Annotated[str | None, Query(description="Filter by organization status.")] = None,
    owner_id: Annotated[UUID | None, Query(description="Filter by owner UUID.")] = None,
    city: Annotated[str | None, Query(description="Filter by city.")] = None,
    country: Annotated[str | None, Query(description="Filter by country.")] = None,
    organization_type: Annotated[
        str | None,
        Query(description="Filter by organization type."),
    ] = None,
    email: Annotated[str | None, Query(description="Filter by contact email.")] = None,
) -> OrganizationListResponse:
    filters = _build_filters(
        name=name,
        slug=slug,
        status=status,
        owner_id=owner_id,
        city=city,
        country=country,
        organization_type=organization_type,
        email=email,
    )
    return service.search(
        q,
        page=page,
        page_size=page_size,
        filters=filters or None,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
    summary="Get organization",
    description="Return a single organization by its UUID.",
)
def get_organization(
    organization_id: UUID,
    service: Annotated[OrganizationService, Depends(get_organization_service)],
    _user: ReadOrganization,
) -> OrganizationResponse:
    organization = service.get(organization_id)
    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found.")
    return organization


@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create organization",
    description="Create a new organization after validating slug, owner, status, and duplicate name rules.",
)
def create_organization(
    payload: OrganizationCreate,
    service: Annotated[OrganizationService, Depends(get_organization_service)],
    _user: ManageOrganization,
) -> OrganizationResponse:
    return service.create(payload)


@router.put(
    "/{organization_id}",
    response_model=OrganizationResponse,
    summary="Update organization",
    description="Update an organization, including archiving it by setting status to archived.",
)
def update_organization(
    organization_id: UUID,
    payload: OrganizationUpdate,
    service: Annotated[OrganizationService, Depends(get_organization_service)],
    _user: ManageOrganization,
) -> OrganizationResponse:
    organization = service.update(organization_id, payload)
    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found.")
    return organization


@router.delete(
    "/{organization_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Delete organization",
    description="Permanently delete an organization.",
)
def delete_organization(
    organization_id: UUID,
    service: Annotated[OrganizationService, Depends(get_organization_service)],
    _user: ManageOrganization,
) -> None:
    deleted = service.delete(organization_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


__all__ = ["router"]
