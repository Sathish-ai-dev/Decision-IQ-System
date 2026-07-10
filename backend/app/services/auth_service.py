from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from functools import lru_cache
from typing import Any, Protocol, TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.config import settings
from app.core.exceptions import AuthenticationException, ValidationException
from app.core.jwt import (
    TokenKind,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_token_expiration,
    verify_token,
)
from app.core.passwords import hash_password, verify_password
from app.models.role import Role, RoleName
from app.models.user import User

if TYPE_CHECKING:
    from redis import Redis


class TokenRevocationStore(Protocol):
    def revoke(self, token_jti: str, expires_at: datetime) -> None: ...

    def is_revoked(self, token_jti: str) -> bool: ...


class InMemoryTokenRevocationStore:
    """In-memory token revocation store for tests and local usage."""

    def __init__(self) -> None:
        self._revoked: dict[str, datetime] = {}

    def revoke(self, token_jti: str, expires_at: datetime) -> None:
        self._revoked[token_jti] = expires_at

    def is_revoked(self, token_jti: str) -> bool:
        expires_at = self._revoked.get(token_jti)
        if expires_at is None:
            return False
        if expires_at <= datetime.now(timezone.utc):
            self._revoked.pop(token_jti, None)
            return False
        return True


class RedisTokenRevocationStore:
    """Redis-backed token revocation store."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def revoke(self, token_jti: str, expires_at: datetime) -> None:
        ttl_seconds = max(int((expires_at - datetime.now(timezone.utc)).total_seconds()), 1)
        self._client.setex(self._key(token_jti), ttl_seconds, "1")

    def is_revoked(self, token_jti: str) -> bool:
        return bool(self._client.exists(self._key(token_jti)))

    @staticmethod
    def _key(token_jti: str) -> str:
        return f"auth:revoked:{token_jti}"


@lru_cache(maxsize=1)
def get_redis_client() -> Any:
    if not settings.redis_url:
        raise ValueError("REDIS_URL is not configured.")
    try:
        from redis import Redis
    except ImportError as exc:  # pragma: no cover - depends on local environment
        raise ImportError(
            "The 'redis' package is required for RedisTokenRevocationStore."
        ) from exc

    return Redis.from_url(settings.redis_url, decode_responses=True)


def get_token_revocation_store() -> TokenRevocationStore:
    return RedisTokenRevocationStore(get_redis_client())


class RoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: RoleName
    permissions: list["PermissionRead"] = Field(default_factory=list)


class PermissionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    resource: str
    action: str


class AuthenticatedUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    full_name: str
    avatar_url: str | None = None
    status: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    roles: list[RoleRead] = Field(default_factory=list)


class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    access_token_expires_at: datetime
    refresh_token_expires_at: datetime


class AuthSession(AuthTokens):
    user: AuthenticatedUser


@dataclass(slots=True)
class AuthenticationService:
    """Application authentication workflows."""

    session: Session
    revocation_store: TokenRevocationStore | None = None

    def __post_init__(self) -> None:
        if self.revocation_store is None:
            self.revocation_store = get_token_revocation_store()

    def register(
        self,
        *,
        email: str,
        password: str,
        full_name: str,
        avatar_url: str | None = None,
    ) -> AuthSession:
        normalized_email = self._normalize_email(email)
        if self._get_user_by_email(normalized_email) is not None:
            raise ValidationException("A user with this email already exists.")

        user = User(
            email=normalized_email,
            password_hash=hash_password(password),
            full_name=full_name.strip(),
            avatar_url=avatar_url.strip() if avatar_url else None,
            status="active",
        )
        user.roles.append(self._get_or_create_role(RoleName.CITIZEN))
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return self._issue_session(user)

    def login(self, *, email: str, password: str) -> AuthSession:
        user = self._get_user_by_email(self._normalize_email(email))
        if user is None or user.deleted_at is not None:
            raise AuthenticationException("Invalid email or password.")
        if not verify_password(password, user.password_hash):
            raise AuthenticationException("Invalid email or password.")
        return self._issue_session(user)

    def logout(self, *, access_token: str, refresh_token: str | None = None) -> None:
        self._revoke_token(access_token, expected_type="access", allow_already_revoked=True)
        if refresh_token is not None:
            self._revoke_token(
                refresh_token,
                expected_type="refresh",
                allow_already_revoked=True,
            )

    def refresh_token(self, *, refresh_token: str) -> AuthSession:
        payload = self._decode_token(refresh_token, expected_type="refresh")
        self._ensure_not_revoked(payload["jti"])

        user = self._get_user_by_id(self._parse_user_id(payload["sub"]))
        if user is None or user.deleted_at is not None:
            raise AuthenticationException("User account is unavailable.")

        self._revoke_token(refresh_token, expected_type="refresh")
        return self._issue_session(user)

    def current_user(self, *, access_token: str) -> AuthenticatedUser:
        payload = self._decode_token(access_token, expected_type="access")
        self._ensure_not_revoked(payload["jti"])

        user = self._get_user_by_id(self._parse_user_id(payload["sub"]))
        if user is None or user.deleted_at is not None:
            raise AuthenticationException("User account is unavailable.")
        return AuthenticatedUser.model_validate(user)

    def _issue_session(self, user: User) -> AuthSession:
        access_token = create_access_token(str(user.id))
        refresh_token = create_refresh_token(str(user.id))
        access_token_expires_at = self._require_expiration(access_token)
        refresh_token_expires_at = self._require_expiration(refresh_token)
        return AuthSession(
            user=AuthenticatedUser.model_validate(user),
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expires_at=access_token_expires_at,
            refresh_token_expires_at=refresh_token_expires_at,
        )

    def _get_user_by_email(self, email: str) -> User | None:
        statement = (
            select(User)
            .options(selectinload(User.roles).selectinload(Role.permissions))
            .where(User.email == email)
        )
        return self.session.scalar(statement)

    def _get_user_by_id(self, user_id: UUID) -> User | None:
        statement = (
            select(User)
            .options(selectinload(User.roles).selectinload(Role.permissions))
            .where(User.id == user_id)
        )
        return self.session.scalar(statement)

    def _get_or_create_role(self, role_name: RoleName) -> Role:
        statement = select(Role).where(Role.name == role_name)
        role = self.session.scalar(statement)
        if role is not None:
            return role

        role = Role(name=role_name)
        self.session.add(role)
        self.session.flush()
        return role

    def _decode_token(self, token: str, *, expected_type: TokenKind) -> dict[str, object]:
        if not verify_token(token, verify_token_type=expected_type):
            raise AuthenticationException("Invalid token.")
        return decode_token(token, verify_token_type=expected_type)

    def _revoke_token(
        self,
        token: str,
        *,
        expected_type: TokenKind,
        allow_already_revoked: bool = False,
    ) -> None:
        payload = self._decode_token(token, expected_type=expected_type)
        token_jti = payload.get("jti")
        exp = payload.get("exp")
        if not isinstance(token_jti, str) or not isinstance(exp, int):
            raise AuthenticationException("Invalid token payload.")
        assert self.revocation_store is not None
        if allow_already_revoked and self.revocation_store.is_revoked(token_jti):
            return
        self.revocation_store.revoke(
            token_jti,
            datetime.fromtimestamp(exp, tz=timezone.utc),
        )

    def _ensure_not_revoked(self, token_jti: object) -> None:
        if not isinstance(token_jti, str):
            raise AuthenticationException("Invalid token payload.")
        assert self.revocation_store is not None
        if self.revocation_store.is_revoked(token_jti):
            raise AuthenticationException("Token has been revoked.")

    def _require_expiration(self, token: str) -> datetime:
        expiration = get_token_expiration(token)
        if expiration is None:
            raise AuthenticationException("Token expiration is missing.")
        return expiration

    @staticmethod
    def _normalize_email(email: str) -> str:
        normalized = email.strip().lower()
        if not normalized:
            raise ValidationException("Email cannot be empty.")
        return normalized

    @staticmethod
    def _parse_user_id(value: object) -> UUID:
        if not isinstance(value, str):
            raise AuthenticationException("Invalid token payload.")
        try:
            return UUID(value)
        except ValueError as exc:
            raise AuthenticationException("Invalid token payload.") from exc


__all__ = [
    "AuthSession",
    "AuthTokens",
    "AuthenticatedUser",
    "AuthenticationService",
    "InMemoryTokenRevocationStore",
    "RedisTokenRevocationStore",
    "PermissionRead",
    "RoleRead",
    "TokenRevocationStore",
    "get_redis_client",
    "get_token_revocation_store",
]
