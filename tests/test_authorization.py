from __future__ import annotations

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import select

import app.models  # noqa: F401
from app.api.dependencies import get_auth_service
from app.core.authorization import require_permission, require_role, require_roles
from app.database import Base, SessionLocal, engine
from app.models import Permission, Role, RoleName, User
from app.services.auth_service import AuthenticationService, InMemoryTokenRevocationStore


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
def auth_service(session):
    return AuthenticationService(session, revocation_store=InMemoryTokenRevocationStore())


@pytest.fixture()
def app_with_dependencies(auth_service):
    test_app = FastAPI()

    def override_auth_service() -> AuthenticationService:
        return auth_service

    test_app.dependency_overrides[get_auth_service] = override_auth_service

    @test_app.get("/admin")
    def admin_route(current_user=Depends(require_role(RoleName.ADMIN))):
        return {"email": current_user.email}

    @test_app.get("/documents")
    def document_route(current_user=Depends(require_permission("documents", "read"))):
        return {"email": current_user.email}

    @test_app.get("/analyst")
    def analyst_route(current_user=Depends(require_roles(RoleName.ANALYST, RoleName.ADMIN))):
        return {"email": current_user.email}

    return test_app


@pytest.fixture()
def client(app_with_dependencies):
    with TestClient(app_with_dependencies) as test_client:
        yield test_client


def test_role_dependency_blocks_unauthorized_user(client: TestClient, session, auth_service) -> None:
    registered = auth_service.register(
        email="frank@example.com",
        password="strong-password",
        full_name="Frank Example",
    )

    response = client.get(
        "/admin",
        headers={"Authorization": f"Bearer {registered.access_token}"},
    )

    assert response.status_code == 403


def test_role_and_permission_dependencies_allow_authorized_user(
    client: TestClient,
    session,
    auth_service,
) -> None:
    registered = auth_service.register(
        email="grace@example.com",
        password="strong-password",
        full_name="Grace Example",
    )

    user = session.get(User, registered.user.id)
    assert user is not None

    admin_role = session.scalar(select(Role).where(Role.name == RoleName.ADMIN))
    if admin_role is None:
        admin_role = Role(name=RoleName.ADMIN)
        session.add(admin_role)
        session.flush()

    admin_role.permissions.append(Permission(resource="documents", action="read"))
    user.roles.append(admin_role)
    session.commit()

    admin_response = client.get(
        "/admin",
        headers={"Authorization": f"Bearer {registered.access_token}"},
    )
    assert admin_response.status_code == 200

    analyst_response = client.get(
        "/analyst",
        headers={"Authorization": f"Bearer {registered.access_token}"},
    )
    assert analyst_response.status_code == 200

    documents_response = client.get(
        "/documents",
        headers={"Authorization": f"Bearer {registered.access_token}"},
    )
    assert documents_response.status_code == 200
