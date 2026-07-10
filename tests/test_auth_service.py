from __future__ import annotations

import pytest

import app.models  # noqa: F401
from app.core.exceptions import AuthenticationException, ValidationException
from app.core.jwt import verify_token
from app.database import Base, SessionLocal, engine
from app.services.auth_service import (
    AuthenticationService,
    InMemoryTokenRevocationStore,
)


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


def test_register_login_refresh_current_user_and_logout(session) -> None:
    service = AuthenticationService(
        session,
        revocation_store=InMemoryTokenRevocationStore(),
    )

    registered = service.register(
        email="alice@example.com",
        password="strong-password",
        full_name="Alice Example",
    )

    assert registered.user.email == "alice@example.com"
    assert registered.user.roles[0].name.value == "Citizen"
    assert verify_token(registered.access_token, verify_token_type="access") is True

    current_user = service.current_user(access_token=registered.access_token)
    assert current_user.email == "alice@example.com"
    assert current_user.roles[0].name.value == "Citizen"

    logged_in = service.login(
        email="alice@example.com",
        password="strong-password",
    )
    refreshed = service.refresh_token(refresh_token=logged_in.refresh_token)

    assert refreshed.user.id == registered.user.id
    assert refreshed.access_token != logged_in.access_token
    assert refreshed.refresh_token != logged_in.refresh_token

    service.logout(
        access_token=refreshed.access_token,
        refresh_token=refreshed.refresh_token,
    )

    with pytest.raises(AuthenticationException):
        service.current_user(access_token=refreshed.access_token)

    with pytest.raises(AuthenticationException):
        service.refresh_token(refresh_token=refreshed.refresh_token)


def test_register_rejects_duplicate_email(session) -> None:
    service = AuthenticationService(
        session,
        revocation_store=InMemoryTokenRevocationStore(),
    )

    service.register(
        email="bob@example.com",
        password="strong-password",
        full_name="Bob Example",
    )

    with pytest.raises(ValidationException):
        service.register(
            email="bob@example.com",
            password="another-password",
            full_name="Bob Example 2",
        )


def test_login_rejects_wrong_password(session) -> None:
    service = AuthenticationService(
        session,
        revocation_store=InMemoryTokenRevocationStore(),
    )

    service.register(
        email="carol@example.com",
        password="strong-password",
        full_name="Carol Example",
    )

    with pytest.raises(AuthenticationException):
        service.login(email="carol@example.com", password="wrong-password")
