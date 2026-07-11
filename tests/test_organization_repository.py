from __future__ import annotations

from uuid import UUID, uuid4

import pytest

from app.database.base import Base
from app.database.engine import engine
from app.database.session import SessionLocal
from app.models.user import User
from app.modules.organizations.models import Organization
from app.modules.organizations.repository import OrganizationRepository


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


def _create_owner(session, owner_id: UUID | None = None) -> User:
    user = User(
        id=owner_id or uuid4(),
        email=f"owner-{uuid4().hex[:8]}@example.com",
        password_hash="hash",
        full_name="Owner",
        status="active",
    )
    session.add(user)
    session.flush()
    return user


def _create_organization(
    session,
    *,
    name: str,
    slug: str,
    status: str = "active",
    owner_id: UUID | None = None,
) -> Organization:
    owner = _create_owner(session, owner_id=owner_id)
    organization = Organization(
        name=name,
        slug=slug,
        status=status,
        owner_id=owner.id,
    )
    session.add(organization)
    session.flush()
    return organization


def test_create_get_and_slug_lookup(session) -> None:
    repository = OrganizationRepository(session)
    organization = Organization(
        name="Decision IQ",
        slug="decision-iq",
        status="active",
        owner_id=_create_owner(session).id,
    )

    created = repository.create(organization)

    assert created.id is not None
    assert repository.get_by_id(created.id) is created
    assert repository.get_by_slug("decision-iq") is created


def test_list_supports_filtering_pagination_and_sorting(session) -> None:
    repository = OrganizationRepository(session)
    _create_organization(session, name="Charlie Org", slug="charlie-org", status="active")
    _create_organization(session, name="Alpha Org", slug="alpha-org", status="active")
    _create_organization(session, name="Bravo Org", slug="bravo-org", status="archived")

    items, meta = repository.list(
        page=1,
        page_size=2,
        filters={"status": "active"},
        sort_by="name",
        sort_order="asc",
    )

    assert [item.name for item in items] == ["Alpha Org", "Charlie Org"]
    assert meta.page == 1
    assert meta.page_size == 2
    assert meta.total_items == 2
    assert meta.total_pages == 1
    assert meta.has_next is False
    assert meta.has_previous is False


def test_search_supports_filters_and_sorting(session) -> None:
    repository = OrganizationRepository(session)
    _create_organization(session, name="North Star Analytics", slug="north-star", status="active")
    _create_organization(session, name="Northbound Research", slug="northbound", status="active")
    _create_organization(session, name="South Horizon", slug="south-horizon", status="active")

    items, meta = repository.search(
        "north",
        page=1,
        page_size=10,
        filters={"status": "active"},
        sort_by="slug",
        sort_order="asc",
    )

    assert [item.slug for item in items] == ["north-star", "northbound"]
    assert meta.total_items == 2
    assert meta.total_pages == 1


def test_update_and_delete(session) -> None:
    repository = OrganizationRepository(session)
    organization = _create_organization(
        session,
        name="Old Name",
        slug="old-name",
        status="active",
    )

    updated = repository.update(organization.id, name="New Name", slug="new-name")
    assert updated is not None
    assert updated.name == "New Name"
    assert repository.get_by_slug("new-name") is updated

    deleted = repository.delete(organization.id)
    assert deleted is True
    assert repository.get_by_id(organization.id) is None


def test_rejects_invalid_sort_and_filter_fields(session) -> None:
    repository = OrganizationRepository(session)
    _create_organization(session, name="Alpha", slug="alpha")

    with pytest.raises(ValueError):
        repository.list(sort_by="not_a_column")

    with pytest.raises(ValueError):
        repository.list(filters={"not_a_column": "value"})
