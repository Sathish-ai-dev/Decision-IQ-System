from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException as FastAPIHTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.shared.responses.error import ApiErrorResponse, StandardErrorResponse


class StandardAPIError(BaseModel):
    """Standard error payload used by the application."""

    model_config = ConfigDict(extra="forbid")

    success: bool = Field(default=False, frozen=True)
    message: str = Field(default="Request failed.")
    errors: list[ApiErrorResponse] = Field(default_factory=list)
    data: None = Field(default=None)
    meta: dict[str, Any] | None = Field(default=None)


class AppException(Exception):
    """Base exception for application-specific errors."""

    status_code: int = 500
    error_type: str = "about:blank"
    title: str = "Request failed."

    def __init__(
        self,
        detail: str | None = None,
        *,
        status_code: int | None = None,
        title: str | None = None,
        error_type: str | None = None,
        errors: Sequence[Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code or self.status_code
        self.title = title or self.title
        self.error_type = error_type or self.error_type
        self.errors = list(errors or [])
        self.headers = dict(headers or {})
        self.request_id = str(uuid4())


class ValidationException(AppException):
    """Raised when application-level validation fails."""

    status_code = 422
    error_type = "https://httpstatuses.com/422"
    title = "Validation failed."


class AuthenticationException(AppException):
    """Raised when authentication is missing or invalid."""

    status_code = 401
    error_type = "https://httpstatuses.com/401"
    title = "Authentication required."


class DatabaseException(AppException):
    """Raised when database access fails."""

    status_code = 500
    error_type = "https://httpstatuses.com/500"
    title = "Database error."


class HTTPException(AppException):
    """Application HTTP exception with an explicit status code."""

    error_type = "about:blank"

    def __init__(
        self,
        status_code: int,
        detail: str | None = None,
        *,
        title: str | None = None,
        error_type: str | None = None,
        errors: Sequence[Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(
            detail,
            status_code=status_code,
            title=title or "Request failed.",
            error_type=error_type,
            errors=errors,
            headers=headers,
        )


def _build_error_response(
    *,
    status_code: int,
    message: str,
    title: str,
    detail: str | None = None,
    error_type: str = "about:blank",
    errors: Sequence[Any] | None = None,
    instance: str | None = None,
    headers: Mapping[str, str] | None = None,
) -> JSONResponse:
    payload = StandardErrorResponse(
        message=message,
        errors=[
            ApiErrorResponse(
                type=error_type,
                title=title,
                status=status_code,
                detail=detail,
                instance=instance,
                errors=list(errors or []),
            )
        ],
    )
    return JSONResponse(
        status_code=status_code,
        content=payload.model_dump(mode="json"),
        headers=dict(headers or {}),
    )


def _extract_validation_errors(errors: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    extracted: list[dict[str, Any]] = []
    for error in errors:
        extracted.append(
            {
                "type": error.get("type"),
                "loc": list(error.get("loc", [])),
                "msg": error.get("msg"),
                "input": error.get("input"),
                "ctx": error.get("ctx"),
            }
        )
    return extracted


def _extract_custom_validation_errors(errors: Sequence[Any]) -> list[Any]:
    return list(errors)


def _render_exception(
    *,
    status_code: int,
    title: str,
    detail: str | None,
    error_type: str,
    errors: Sequence[Any] | None = None,
    headers: Mapping[str, str] | None = None,
    request: Request | None = None,
) -> JSONResponse:
    instance = str(request.url) if request is not None else None
    return _build_error_response(
        status_code=status_code,
        message=detail or title,
        title=title,
        detail=detail,
        error_type=error_type,
        errors=errors,
        instance=instance,
        headers=headers,
    )


async def handle_app_exception(request: Request, exc: AppException) -> JSONResponse:
    return _render_exception(
        request=request,
        status_code=exc.status_code,
        title=exc.title,
        detail=exc.detail,
        error_type=exc.error_type,
        errors=exc.errors,
        headers=exc.headers,
    )


async def handle_validation_exception(
    request: Request,
    exc: RequestValidationError | ValidationException,
) -> JSONResponse:
    if isinstance(exc, RequestValidationError):
        errors = _extract_validation_errors(exc.errors())
        detail = "Request validation failed."
        error_type = "https://httpstatuses.com/422"
    else:
        errors = _extract_custom_validation_errors(exc.errors)
        detail = exc.detail or "Validation failed."
        error_type = exc.error_type
    return _render_exception(
        request=request,
        status_code=422,
        title="Validation failed.",
        detail=detail,
        error_type=error_type,
        errors=errors,
    )


async def handle_authentication_exception(
    request: Request,
    exc: AuthenticationException,
) -> JSONResponse:
    return await handle_app_exception(request, exc)


async def handle_database_exception(
    request: Request,
    exc: DatabaseException,
) -> JSONResponse:
    return await handle_app_exception(request, exc)


async def handle_http_exception(
    request: Request,
    exc: FastAPIHTTPException | StarletteHTTPException,
) -> JSONResponse:
    title = "HTTP error."
    if getattr(exc, "detail", None):
        title = "Request failed."
    return _render_exception(
        request=request,
        status_code=exc.status_code,
        title=title,
        detail=str(exc.detail) if exc.detail is not None else None,
        error_type="about:blank",
        headers=getattr(exc, "headers", None),
    )


async def handle_sqlalchemy_exception(
    request: Request,
    exc: SQLAlchemyError,
) -> JSONResponse:
    return _render_exception(
        request=request,
        status_code=500,
        title="Database error.",
        detail="An unexpected database error occurred.",
        error_type="https://httpstatuses.com/500",
        errors=[exc.__class__.__name__],
    )


async def handle_unhandled_exception(request: Request, exc: Exception) -> JSONResponse:
    return _render_exception(
        request=request,
        status_code=500,
        title="Internal server error.",
        detail="An unexpected error occurred.",
        error_type="https://httpstatuses.com/500",
        errors=[exc.__class__.__name__],
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all standardized application exception handlers."""

    app.add_exception_handler(AppException, handle_app_exception)
    app.add_exception_handler(ValidationException, handle_validation_exception)
    app.add_exception_handler(AuthenticationException, handle_authentication_exception)
    app.add_exception_handler(DatabaseException, handle_database_exception)
    app.add_exception_handler(FastAPIHTTPException, handle_http_exception)
    app.add_exception_handler(StarletteHTTPException, handle_http_exception)
    app.add_exception_handler(RequestValidationError, handle_validation_exception)
    app.add_exception_handler(SQLAlchemyError, handle_sqlalchemy_exception)
    app.add_exception_handler(Exception, handle_unhandled_exception)


__all__ = [
    "AppException",
    "AuthenticationException",
    "DatabaseException",
    "HTTPException",
    "StandardAPIError",
    "ValidationException",
    "handle_app_exception",
    "handle_authentication_exception",
    "handle_database_exception",
    "handle_http_exception",
    "handle_sqlalchemy_exception",
    "handle_unhandled_exception",
    "handle_validation_exception",
    "register_exception_handlers",
]
