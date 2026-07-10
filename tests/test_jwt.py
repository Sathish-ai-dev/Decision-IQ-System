from __future__ import annotations

from datetime import timedelta

from app.core.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_token_expiration,
    is_token_expired,
    verify_token,
)


def test_create_access_token_round_trip() -> None:
    token = create_access_token(
        "user-123",
        expires_delta=timedelta(minutes=5),
        additional_claims={"scope": "read"},
    )

    payload = decode_token(token)

    assert payload["sub"] == "user-123"
    assert payload["type"] == "access"
    assert payload["scope"] == "read"
    assert get_token_expiration(token) is not None
    assert verify_token(token, verify_token_type="access") is True
    assert is_token_expired(token) is False


def test_create_refresh_token_has_refresh_type() -> None:
    access_token = create_access_token("user-123", expires_delta=timedelta(minutes=5))
    refresh_token = create_refresh_token(
        "user-123",
        expires_delta=timedelta(minutes=10),
    )

    access_exp = get_token_expiration(access_token)
    refresh_exp = get_token_expiration(refresh_token)

    assert decode_token(refresh_token)["type"] == "refresh"
    assert verify_token(refresh_token, verify_token_type="refresh") is True
    assert verify_token(access_token, verify_token_type="refresh") is False
    assert access_exp is not None
    assert refresh_exp is not None
    assert refresh_exp > access_exp


def test_expired_token_is_reported_as_expired() -> None:
    token = create_access_token("user-123", expires_delta=timedelta(seconds=-1))

    assert verify_token(token) is False
    assert is_token_expired(token) is True
    assert decode_token(token, verify_expiration=False)["sub"] == "user-123"
