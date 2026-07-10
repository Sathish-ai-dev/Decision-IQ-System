from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict, Field

from app.api.dependencies import get_access_token, get_auth_service
from app.services.auth_service import AuthSession, AuthenticatedUser, AuthenticationService


router = APIRouter(prefix="/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: str = Field(min_length=1)
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=1)
    avatar_url: str | None = None


class RefreshRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    refresh_token: str = Field(min_length=1)


class LogoutRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    refresh_token: str | None = None


class MeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user: AuthenticatedUser


@router.post("/login", response_model=AuthSession)
def login(
    payload: LoginRequest,
    service: Annotated[AuthenticationService, Depends(get_auth_service)],
) -> AuthSession:
    return service.login(email=payload.email, password=payload.password)


@router.post("/register", response_model=AuthSession, status_code=status.HTTP_201_CREATED)
def register(
    payload: RegisterRequest,
    service: Annotated[AuthenticationService, Depends(get_auth_service)],
) -> AuthSession:
    return service.register(
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
        avatar_url=payload.avatar_url,
    )


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    payload: LogoutRequest,
    service: Annotated[AuthenticationService, Depends(get_auth_service)],
    access_token: Annotated[str, Depends(get_access_token)],
) -> None:
    service.logout(access_token=access_token, refresh_token=payload.refresh_token)


@router.post("/refresh", response_model=AuthSession)
def refresh(
    payload: RefreshRequest,
    service: Annotated[AuthenticationService, Depends(get_auth_service)],
) -> AuthSession:
    return service.refresh_token(refresh_token=payload.refresh_token)


@router.get("/me", response_model=MeResponse)
def me(
    service: Annotated[AuthenticationService, Depends(get_auth_service)],
    access_token: Annotated[str, Depends(get_access_token)],
) -> MeResponse:
    return MeResponse(user=service.current_user(access_token=access_token))
