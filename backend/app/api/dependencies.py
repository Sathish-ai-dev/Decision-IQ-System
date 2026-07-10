from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.services.auth_service import AuthenticatedUser, AuthenticationService


def get_auth_service(db: Annotated[Session, Depends(get_db)]) -> AuthenticationService:
    return AuthenticationService(db)


def get_access_token(authorization: Annotated[str | None, Header()] = None) -> str:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is required.",
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header must use the Bearer scheme.",
        )

    return token.strip()


def get_current_user(
    access_token: Annotated[str, Depends(get_access_token)],
    service: Annotated[AuthenticationService, Depends(get_auth_service)],
) -> AuthenticatedUser:
    return service.current_user(access_token=access_token)
