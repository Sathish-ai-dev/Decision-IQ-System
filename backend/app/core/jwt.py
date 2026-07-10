from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Literal
from uuid import uuid4

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from app.core.config import settings


TokenKind = Literal["access", "refresh"]


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _expiration_for_token_type(
    token_type: TokenKind,
    expires_delta: timedelta | None = None,
) -> timedelta:
    if expires_delta is not None:
        return expires_delta
    if token_type == "access":
        return timedelta(minutes=settings.jwt_access_token_expiry_minutes)
    return timedelta(days=settings.jwt_refresh_token_expiry_days)


def _build_claims(
    subject: str,
    token_type: TokenKind,
    *,
    expires_delta: timedelta | None = None,
    additional_claims: dict[str, Any] | None = None,
) -> dict[str, Any]:
    now = _utcnow()
    expiry = now + _expiration_for_token_type(token_type, expires_delta)

    claims: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "jti": uuid4().hex,
        "iat": int(now.timestamp()),
        "exp": int(expiry.timestamp()),
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
    }
    if additional_claims:
        claims.update(additional_claims)
    return claims


def _encode_token(claims: dict[str, Any]) -> str:
    return jwt.encode(
        claims,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def create_access_token(
    subject: str,
    *,
    expires_delta: timedelta | None = None,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    """Create a signed access token for the given subject."""

    claims = _build_claims(
        subject,
        "access",
        expires_delta=expires_delta,
        additional_claims=additional_claims,
    )
    return _encode_token(claims)


def create_refresh_token(
    subject: str,
    *,
    expires_delta: timedelta | None = None,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    """Create a signed refresh token for the given subject."""

    claims = _build_claims(
        subject,
        "refresh",
        expires_delta=expires_delta,
        additional_claims=additional_claims,
    )
    return _encode_token(claims)


def decode_token(
    token: str,
    *,
    verify_expiration: bool = True,
    verify_token_type: TokenKind | None = None,
) -> dict[str, Any]:
    """Decode and optionally verify a JWT payload."""

    options = {"verify_exp": verify_expiration}
    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
        audience=settings.jwt_audience,
        issuer=settings.jwt_issuer,
        options=options,
    )

    if verify_token_type is not None and payload.get("type") != verify_token_type:
        raise InvalidTokenError("Unexpected token type.")

    return payload


def verify_token(
    token: str,
    *,
    verify_token_type: TokenKind | None = None,
) -> bool:
    """Return True when the token is valid and not expired."""

    try:
        decode_token(token, verify_expiration=True, verify_token_type=verify_token_type)
        return True
    except (ExpiredSignatureError, InvalidTokenError):
        return False


def get_token_expiration(token: str) -> datetime | None:
    """Return the token expiration time, ignoring expiration validation."""

    try:
        payload = decode_token(token, verify_expiration=False)
    except InvalidTokenError:
        return None

    exp = payload.get("exp")
    if exp is None:
        return None
    return datetime.fromtimestamp(int(exp), tz=timezone.utc)


def is_token_expired(token: str) -> bool:
    """Return True when the token has expired or is invalid."""

    exp = get_token_expiration(token)
    if exp is None:
        return True
    return exp <= _utcnow()
