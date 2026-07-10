from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.api.dependencies import get_current_user
from app.models.role import RoleName
from app.services.auth_service import AuthenticatedUser


@dataclass(frozen=True, slots=True)
class PermissionSpec:
    resource: str
    action: str


def _normalize(value: str) -> str:
    return value.strip().lower()


def _matches_pattern(candidate: str, pattern: str) -> bool:
    normalized_candidate = _normalize(candidate)
    normalized_pattern = _normalize(pattern)
    return normalized_pattern == "*" or normalized_candidate == normalized_pattern


def user_has_role(user: AuthenticatedUser, *roles: RoleName | str) -> bool:
    required_roles = {_normalize(role.value if isinstance(role, RoleName) else role) for role in roles}
    if not required_roles:
        return False

    for role in user.roles:
        if _normalize(role.name.value) in required_roles:
            return True
    return False


def user_has_permission(
    user: AuthenticatedUser,
    *,
    resource: str,
    action: str,
) -> bool:
    for role in user.roles:
        for permission in role.permissions:
            if _matches_pattern(permission.resource, resource) and _matches_pattern(
                permission.action,
                action,
            ):
                return True
    return False


def require_roles(*roles: RoleName | str) -> Callable[[AuthenticatedUser], AuthenticatedUser]:
    if not roles:
        raise ValueError("At least one role is required.")

    def dependency(
        current_user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    ) -> AuthenticatedUser:
        if not user_has_role(current_user, *roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have the required role.",
            )
        return current_user

    return dependency


def require_role(role: RoleName | str) -> Callable[[AuthenticatedUser], AuthenticatedUser]:
    return require_roles(role)


def require_permissions(
    *permissions: PermissionSpec | tuple[str, str],
) -> Callable[[AuthenticatedUser], AuthenticatedUser]:
    if not permissions:
        raise ValueError("At least one permission is required.")

    normalized_permissions = tuple(
        permission
        if isinstance(permission, PermissionSpec)
        else PermissionSpec(resource=permission[0], action=permission[1])
        for permission in permissions
    )

    def dependency(
        current_user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    ) -> AuthenticatedUser:
        if not any(
            user_has_permission(
                current_user,
                resource=permission.resource,
                action=permission.action,
            )
            for permission in normalized_permissions
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have the required permission.",
            )
        return current_user

    return dependency


def require_permission(
    resource: str,
    action: str,
) -> Callable[[AuthenticatedUser], AuthenticatedUser]:
    return require_permissions((resource, action))


__all__ = [
    "PermissionSpec",
    "require_permission",
    "require_permissions",
    "require_role",
    "require_roles",
    "user_has_permission",
    "user_has_role",
]
