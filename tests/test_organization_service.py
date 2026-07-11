from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

import pytest

import app.models  # noqa: F401
from app.core.exceptions import ValidationException
from app.database.base import Base
from app.database.engine import engine
from app.database.session import SessionLocal
from app.models.user import User
from app.modules.organizations.repository import OrganizationRepository
from app.modules.organizations.schemas import OrganizationCreate, OrganizationUpdate
from app.modules.organizations.service import OrganizationService


@pytest.fixture(scope="module", autouse=True)
def create_schema() -> None:
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


def _create_owner(session, *, deleted: bool = False) -> User:
    user = User(
        email=f"owner-{uuid4().hex[:8]}@example.com",
        password_hash="hash",
        full_name="Owner",
        status="active",
    )
    session.add(user)
    session.flush()
    if deleted:
        user.deleted_at = datetime.now(timezone.utc)
        session.flush()
    return user


def _service(session) -> OrganizationService:
    return OrganizationService(session, repository=OrganizationRepository(session))


def test_create_enforces_unique_slug_name_owner_and_status(session) -> None:
    service = _service(session)
    owner = _create_owner(session)

    created = service.create(
        OrganizationCreate(
            name="Decision IQ",
            slug="decision-iq",
            owner_id=owner.id,
            status="active",
            email="team@decisioniq.example",
            website="https://decisioniq.example",
        )
    )

    assert created.slug == "decision-iq"
    assert created.status == "active"

    with pytest.raises(ValidationException):
        service.create(
            OrganizationCreate(
                name="Decision IQ",
                slug="different-slug",
                owner_id=owner.id,
            )
        )

    with pytest.raises(ValidationException):
        service.create(
            OrganizationCreate(
                name="Another Organization",
                slug="decision-iq",
                owner_id=owner.id,
            )
        )

    with pytest.raises(ValidationException):
        service.create(
            OrganizationCreate(
                name="Bad Owner Org",
                slug="bad-owner-org",
                owner_id=uuid4(),
            )
        )

    with pytest.raises(ValidationException):
        service.create(
            OrganizationCreate(
                name="Bad Status Org",
                slug="bad-status-org",
                owner_id=owner.id,
                status="unknown",
            )
        )


def test_create_rejects_deleted_owner(session) -> None:
    service = _service(session)
    owner = _create_owner(session, deleted=True)

    with pytest.raises(ValidationException):
        service.create(
            OrganizationCreate(
                name="Deleted Owner Org",
                slug="deleted-owner-org",
                owner_id=owner.id,
            )
        )


def test_search_service_and_archive_support(session) -> None:
    service = _service(session)
    owner = _create_owner(session)

    service.create(
        OrganizationCreate(
            name="North Star Analytics",
            slug="north-star",
            owner_id=owner.id,
            status="active",
        )
    )
    created = service.create(
        OrganizationCreate(
            name="South Horizon",
            slug="south-horizon",
            owner_id=owner.id,
            status="active",
        )
    )

    archived = service.archive(created.id)
    assert archived is not None
    assert archived.status == "archived"

    result = service.search(
        "north",
        filters={"status": "active"},
        sort_by="name",
        sort_order="asc",
    )
    assert [item.slug for item in result.data] == ["north-star"]

    archived_result = service.list(filters={"status": "archived"})
    assert [item.slug for item in archived_result.data] == ["south-horizon"]


def test_update_rejects_duplicate_name_and_can_clear_fields(session) -> None:
    service = _service(session)
    owner = _create_owner(session)

    first = service.create(
        OrganizationCreate(
            name="Alpha Org",
            slug="alpha-org",
            owner_id=owner.id,
            description="First",
        )
    )
    second = service.create(
        OrganizationCreate(
            name="Beta Org",
            slug="beta-org",
            owner_id=owner.id,
            description="Second",
        )
    )

    with pytest.raises(ValidationException):
        service.update(
            second.id,
            OrganizationUpdate(name="Alpha Org"),
        )

    updated = service.update(
        first.id,
        OrganizationUpdate(description=None, status="draft"),
    )
    assert updated is not None
    assert updated.description is None
    assert updated.status == "draft"


def test_archive_missing_organization_returns_none(session) -> None:
    service = _service(session)

    assert service.archive(uuid4()) is None
