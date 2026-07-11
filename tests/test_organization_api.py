from __future__ import annotations

from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

import app.models  # noqa: F401
from app.api.dependencies import get_auth_service, get_db
from app.database.base import Base
from app.database.engine import engine
from app.database.session import SessionLocal
from app.models import Role, RoleName, User
from app.services.auth_service import AuthenticationService, InMemoryTokenRevocationStore
from main import app


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


@pytest.fixture()
def client(session):
    store = InMemoryTokenRevocationStore()

    def override_auth_service() -> AuthenticationService:
        return AuthenticationService(session, revocation_store=store)

    def override_db():
        yield session

    app.dependency_overrides[get_auth_service] = override_auth_service
    app.dependency_overrides[get_db] = override_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def _register_admin(session, client: TestClient) -> tuple[str, str, str]:
    email = f"org-admin-{uuid4().hex[:8]}@example.com"
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "strong-password",
            "full_name": "Org Admin",
        },
    )
    assert response.status_code == 201
    payload = response.json()

    user = session.get(User, UUID(payload["user"]["id"]))
    assert user is not None

    admin_role = session.scalar(select(Role).where(Role.name == RoleName.ADMIN))
    if admin_role is None:
        admin_role = Role(name=RoleName.ADMIN)
        session.add(admin_role)
        session.flush()

    if admin_role not in user.roles:
        user.roles.append(admin_role)
    session.commit()

    return payload["access_token"], payload["refresh_token"], payload["user"]["id"]


def test_organization_crud_search_and_docs(client: TestClient, session) -> None:
    access_token, _, owner_id = _register_admin(session, client)
    headers = {"Authorization": f"Bearer {access_token}"}

    create_response = client.post(
        "/api/v1/organizations",
        headers=headers,
        json={
            "name": "Decision IQ",
            "slug": "decision-iq",
            "owner_id": owner_id,
            "status": "active",
            "email": "team@decisioniq.example",
            "website": "https://decisioniq.example",
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()
    organization_id = created["id"]

    get_response = client.get(f"/api/v1/organizations/{organization_id}", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["slug"] == "decision-iq"

    update_response = client.put(
        f"/api/v1/organizations/{organization_id}",
        headers=headers,
        json={"status": "archived", "description": "Archived workspace"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "archived"

    second_response = client.post(
        "/api/v1/organizations",
        headers=headers,
        json={
            "name": "North Star Analytics",
            "slug": "north-star-analytics",
            "owner_id": owner_id,
            "status": "active",
        },
    )
    assert second_response.status_code == 201

    third_response = client.post(
        "/api/v1/organizations",
        headers=headers,
        json={
            "name": "South Horizon",
            "slug": "south-horizon",
            "owner_id": owner_id,
            "status": "active",
        },
    )
    assert third_response.status_code == 201

    list_response = client.get(
        "/api/v1/organizations",
        headers=headers,
        params={"page": 1, "page_size": 2, "sort_by": "name", "sort_order": "asc"},
    )
    assert list_response.status_code == 200
    list_payload = list_response.json()
    assert list_payload["meta"]["total_items"] == 3
    assert list_payload["meta"]["total_pages"] == 2
    assert list_payload["meta"]["has_next"] is True
    assert list_payload["meta"]["has_previous"] is False
    assert [item["slug"] for item in list_payload["data"]] == [
        "decision-iq",
        "north-star-analytics",
    ]

    second_page = client.get(
        "/api/v1/organizations",
        headers=headers,
        params={"page": 2, "page_size": 2, "sort_by": "name", "sort_order": "asc"},
    )
    assert second_page.status_code == 200
    second_page_payload = second_page.json()
    assert second_page_payload["meta"]["has_next"] is False
    assert second_page_payload["meta"]["has_previous"] is True
    assert [item["slug"] for item in second_page_payload["data"]] == ["south-horizon"]

    search_response = client.get(
        "/api/v1/organizations/search",
        headers=headers,
        params={"q": "north", "status": "active", "sort_by": "slug"},
    )
    assert search_response.status_code == 200
    assert [item["slug"] for item in search_response.json()["data"]] == [
        "north-star-analytics",
    ]

    delete_response = client.delete(f"/api/v1/organizations/{organization_id}", headers=headers)
    assert delete_response.status_code == 204

    missing_response = client.get(f"/api/v1/organizations/{organization_id}", headers=headers)
    assert missing_response.status_code == 404


def test_organization_validation_errors(client: TestClient, session) -> None:
    access_token, _, owner_id = _register_admin(session, client)
    headers = {"Authorization": f"Bearer {access_token}"}

    invalid_slug_response = client.post(
        "/api/v1/organizations",
        headers=headers,
        json={
            "name": "Validation Org",
            "slug": "Invalid Slug",
            "owner_id": owner_id,
            "status": "active",
        },
    )
    assert invalid_slug_response.status_code == 422

    invalid_website_response = client.post(
        "/api/v1/organizations",
        headers=headers,
        json={
            "name": "Validation Org 2",
            "slug": "validation-org-2",
            "owner_id": owner_id,
            "website": "not-a-url",
            "status": "active",
        },
    )
    assert invalid_website_response.status_code == 422

    invalid_status_response = client.post(
        "/api/v1/organizations",
        headers=headers,
        json={
            "name": "Validation Org 3",
            "slug": "validation-org-3",
            "owner_id": owner_id,
            "status": "unknown",
        },
    )
    assert invalid_status_response.status_code == 422


def test_organizations_enforce_rbac(client: TestClient) -> None:
    email = f"citizen-{uuid4().hex[:8]}@example.com"
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "strong-password",
            "full_name": "Citizen User",
        },
    )
    assert response.status_code == 201
    token = response.json()["access_token"]

    forbidden = client.post(
        "/api/v1/organizations",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Forbidden Org",
            "slug": "forbidden-org",
            "owner_id": str(response.json()["user"]["id"]),
            "status": "active",
        },
    )
    assert forbidden.status_code == 403


def test_organizations_require_authentication(client: TestClient) -> None:
    response = client.get("/api/v1/organizations")
    assert response.status_code == 401


def test_openapi_includes_organizations_paths(client: TestClient) -> None:
    openapi = client.get("/openapi.json")
    assert openapi.status_code == 200
    paths = openapi.json()["paths"]
    assert "/api/v1/organizations" in paths
    assert "/api/v1/organizations/{organization_id}" in paths
    assert "/api/v1/organizations/search" in paths
