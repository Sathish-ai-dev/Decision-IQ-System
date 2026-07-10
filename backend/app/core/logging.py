from __future__ import annotations

import contextvars
import json
import logging
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import settings


REQUEST_ID_CONTEXT: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_id",
    default=None,
)


class RequestContextFilter(logging.Filter):
    """Attach request-scoped context to every log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = REQUEST_ID_CONTEXT.get()
        return True


class ErrorFormatter(logging.Formatter):
    """Render error records with exception details and request context."""

    default_time_format = "%Y-%m-%d %H:%M:%S"

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat()
        parts = [f"{timestamp} [{record.levelname}] {record.name}"]
        request_id = getattr(record, "request_id", None)
        if request_id:
            parts.append(f"request_id={request_id}")
        parts.append(record.getMessage())

        if record.exc_info:
            parts.append("\n".join(traceback.format_exception(*record.exc_info)).rstrip())
        elif record.stack_info:
            parts.append(record.stack_info)

        return " | ".join(parts)


class ConsoleFormatter(logging.Formatter):
    """Human-readable formatter for console output."""

    default_time_format = "%Y-%m-%d %H:%M:%S"

    def format(self, record: logging.LogRecord) -> str:
        if record.levelno >= logging.ERROR:
            return ErrorFormatter().format(record)

        timestamp = datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat()
        parts = [f"{timestamp} [{record.levelname}] {record.name}"]
        request_id = getattr(record, "request_id", None)
        if request_id:
            parts.append(f"request_id={request_id}")
        parts.append(record.getMessage())
        return " | ".join(parts)


class FileFormatter(logging.Formatter):
    """Compact text formatter for log files."""

    default_time_format = "%Y-%m-%d %H:%M:%S"

    def format(self, record: logging.LogRecord) -> str:
        return ConsoleFormatter().format(record)


class JsonFormatter(logging.Formatter):
    """Structured JSON formatter for machine-readable logs."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "process": record.process,
            "thread": record.threadName,
        }

        request_id = getattr(record, "request_id", None)
        if request_id:
            payload["request_id"] = request_id

        if record.exc_info:
            payload["exception"] = self._format_exception(record.exc_info)

        if hasattr(record, "extra_data") and record.extra_data is not None:
            payload["extra"] = record.extra_data

        return json.dumps(payload, ensure_ascii=False, default=str)

    @staticmethod
    def _format_exception(exc_info: tuple[type[BaseException], BaseException, Any]) -> dict[str, Any]:
        exc_type, exc_value, exc_tb = exc_info
        return {
            "type": exc_type.__name__,
            "message": str(exc_value),
            "traceback": traceback.format_exception(exc_type, exc_value, exc_tb),
        }


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    """Log incoming requests with latency and status code information."""

    def __init__(
        self,
        app: Any,
        logger_name: str = "app.request",
        request_id_header: str = "X-Request-ID",
    ) -> None:
        super().__init__(app)
        self.logger = logging.getLogger(logger_name)
        self.request_id_header = request_id_header

    async def dispatch(self, request: Request, call_next: Callable[[Request], Any]) -> Response:
        start = time.perf_counter()
        request_id = request.headers.get(self.request_id_header) or request.headers.get(
            self.request_id_header.lower()
        )
        token = REQUEST_ID_CONTEXT.set(request_id)
        try:
            response = await call_next(request)
            duration_ms = (time.perf_counter() - start) * 1000
            self.logger.info(
                "%s %s -> %s",
                request.method,
                request.url.path,
                response.status_code,
                extra={
                    "extra_data": {
                        "method": request.method,
                        "path": request.url.path,
                        "query_string": request.url.query,
                        "status_code": response.status_code,
                        "duration_ms": round(duration_ms, 2),
                        "client": request.client.host if request.client else None,
                    }
                },
            )
            if request_id and self.request_id_header not in response.headers:
                response.headers[self.request_id_header] = request_id
            return response
        except Exception:
            duration_ms = (time.perf_counter() - start) * 1000
            self.logger.exception(
                "Unhandled exception while processing %s %s",
                request.method,
                request.url.path,
                extra={
                    "extra_data": {
                        "method": request.method,
                        "path": request.url.path,
                        "query_string": request.url.query,
                        "duration_ms": round(duration_ms, 2),
                        "client": request.client.host if request.client else None,
                    }
                },
            )
            raise
        finally:
            REQUEST_ID_CONTEXT.reset(token)


def _build_file_handler(log_path: Path) -> logging.Handler:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setLevel(logging.INFO)
    handler.setFormatter(FileFormatter())
    handler.addFilter(RequestContextFilter())
    return handler


def _build_json_handler(log_path: Path) -> logging.Handler:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setLevel(logging.INFO)
    handler.setFormatter(JsonFormatter())
    handler.addFilter(RequestContextFilter())
    return handler


def configure_logging(
    *,
    log_dir: Path | None = None,
    console_level: int | None = None,
    file_level: int | None = None,
    json_level: int | None = None,
) -> None:
    """Configure application logging once at process start."""

    if log_dir is None:
        log_dir = Path("logs")

    resolved_level = getattr(logging, settings.log_level or "INFO", logging.INFO)
    console_level = console_level or resolved_level
    file_level = file_level or resolved_level
    json_level = json_level or resolved_level

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addFilter(RequestContextFilter())

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(ConsoleFormatter())
    console_handler.addFilter(RequestContextFilter())

    file_handler = _build_file_handler(log_dir / "app.log")
    file_handler.setLevel(file_level)

    json_handler = _build_json_handler(log_dir / "app.jsonl")
    json_handler.setLevel(json_level)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(json_handler)

    logging.captureWarnings(True)

    for noisy_logger in ("uvicorn", "uvicorn.error", "uvicorn.access", "asyncio"):
        logger = logging.getLogger(noisy_logger)
        logger.handlers.clear()
        logger.propagate = True


def get_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(name or "app")


__all__ = [
    "ConsoleFormatter",
    "ErrorFormatter",
    "FileFormatter",
    "JsonFormatter",
    "RequestContextFilter",
    "RequestLoggerMiddleware",
    "configure_logging",
    "get_logger",
    "settings",
]
