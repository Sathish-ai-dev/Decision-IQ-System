from __future__ import annotations

import time
from collections.abc import Awaitable, Callable
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.logging import REQUEST_ID_CONTEXT, get_logger


REQUEST_ID_HEADER = "X-Request-ID"
RESPONSE_TIME_HEADER = "X-Response-Time"
SERVER_TIMING_HEADER = "Server-Timing"


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Assign a request ID and propagate it through the response and logs."""

    def __init__(self, app: Any, header_name: str = REQUEST_ID_HEADER) -> None:
        super().__init__(app)
        self.header_name = header_name

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        request_id = request.headers.get(self.header_name) or request.headers.get(
            self.header_name.lower()
        )
        request_id = request_id.strip() if isinstance(request_id, str) else None
        if not request_id:
            request_id = uuid4().hex

        token = REQUEST_ID_CONTEXT.set(request_id)
        request.state.request_id = request_id
        try:
            response = await call_next(request)
            response.headers[self.header_name] = request_id
            return response
        finally:
            REQUEST_ID_CONTEXT.reset(token)


class RequestTimingMiddleware(BaseHTTPMiddleware):
    """Record total request duration and expose it on the response."""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        response.headers[RESPONSE_TIME_HEADER] = f"{duration_ms:.2f}ms"
        response.headers[SERVER_TIMING_HEADER] = f"app;dur={duration_ms:.2f}"
        request.state.duration_ms = duration_ms
        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log completed requests with metadata and latency."""

    def __init__(self, app: Any, logger_name: str = "app.request") -> None:
        super().__init__(app)
        self.logger = get_logger(logger_name)

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        start = time.perf_counter()
        request_id = getattr(request.state, "request_id", None) or request.headers.get(
            REQUEST_ID_HEADER
        )
        token = None
        if request_id:
            token = REQUEST_ID_CONTEXT.set(request_id)
        try:
            response = await call_next(request)
        except Exception:
            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            if token is None:
                token = REQUEST_ID_CONTEXT.set(request_id or uuid4().hex)
            self.logger.exception(
                "Unhandled exception while processing %s %s",
                request.method,
                request.url.path,
                extra={
                    "extra_data": self._build_extra(
                        request=request,
                        status_code=500,
                        duration_ms=duration_ms,
                    )
                },
            )
            REQUEST_ID_CONTEXT.reset(token)
            raise

        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        if token is None:
            token = REQUEST_ID_CONTEXT.set(request_id or uuid4().hex)
        self.logger.info(
            "%s %s -> %s",
            request.method,
            request.url.path,
            response.status_code,
            extra={
                "extra_data": self._build_extra(
                    request=request,
                    status_code=response.status_code,
                    duration_ms=duration_ms,
                )
            },
        )
        REQUEST_ID_CONTEXT.reset(token)
        return response

    @staticmethod
    def _build_extra(request: Request, status_code: int, duration_ms: float) -> dict[str, Any]:
        return {
            "request_id": getattr(request.state, "request_id", None),
            "method": request.method,
            "path": request.url.path,
            "query_string": request.url.query,
            "status_code": status_code,
            "duration_ms": duration_ms,
            "client": request.client.host if request.client else None,
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        }


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Attach baseline security headers to all responses."""

    @staticmethod
    def security_headers() -> dict[str, str]:
        headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
            "Cross-Origin-Opener-Policy": "same-origin",
            "Cross-Origin-Resource-Policy": "same-origin",
            "X-Permitted-Cross-Domain-Policies": "none",
        }
        if settings.is_production:
            headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return headers

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        response = await call_next(request)
        for name, value in self.security_headers().items():
            response.headers.setdefault(name, value)
        return response


def add_middleware(app: FastAPI) -> None:
    """Install the shared middleware stack."""

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins or [],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=[REQUEST_ID_HEADER, RESPONSE_TIME_HEADER, SERVER_TIMING_HEADER],
        max_age=600,
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(RequestTimingMiddleware)
    app.add_middleware(RequestLoggingMiddleware)


__all__ = [
    "REQUEST_ID_HEADER",
    "RESPONSE_TIME_HEADER",
    "SERVER_TIMING_HEADER",
    "RequestIDMiddleware",
    "RequestLoggingMiddleware",
    "RequestTimingMiddleware",
    "SecurityHeadersMiddleware",
    "add_middleware",
]
