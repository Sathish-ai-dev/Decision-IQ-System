from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

import app.models  # noqa: F401
from app.api.dependencies import get_auth_service
from app.database import Base, SessionLocal, engine
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

    app.dependency_overrides[get_auth_service] = override_auth_service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_register_login_me_refresh_and_logout(client: TestClient) -> None:
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "dana@example.com",
            "password": "strong-password",
            "full_name": "Dana Example",
        },
    )
    assert register_response.status_code == 201
    register_payload = register_response.json()
    access_token = register_payload["access_token"]
    refresh_token = register_payload["refresh_token"]

    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["user"]["email"] == "dana@example.com"

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "dana@example.com", "password": "strong-password"},
    )
    assert login_response.status_code == 200
    login_payload = login_response.json()
    assert login_payload["user"]["email"] == "dana@example.com"

    refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert refresh_response.status_code == 200
    refreshed_payload = refresh_response.json()
    refreshed_access_token = refreshed_payload["access_token"]
    refreshed_refresh_token = refreshed_payload["refresh_token"]
    assert refreshed_payload["user"]["email"] == "dana@example.com"

    logout_response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {refreshed_access_token}"},
        json={"refresh_token": refreshed_refresh_token},
    )
    assert logout_response.status_code == 200

    me_after_logout = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {refreshed_access_token}"},
    )
    assert me_after_logout.status_code == 401


def test_login_rejects_bad_password(client: TestClient) -> None:
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "erin@example.com",
            "password": "strong-password",
            "full_name": "Erin Example",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "erin@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
