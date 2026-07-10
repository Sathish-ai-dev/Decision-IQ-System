from __future__ import annotations

import time
from typing import Literal

from fastapi import FastAPI, Response
from pydantic import BaseModel, ConfigDict, Field

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.core.middleware import add_middleware
from app.database.health import check_database_health
from app.api import auth_router


APP_VERSION = "0.1.0"
START_TIME = time.monotonic()


class HealthResponse(BaseModel):
    """Standard health response payload."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["healthy", "degraded", "unhealthy"]
    version: str = Field(default=APP_VERSION)
    environment: str
    database: Literal["up", "down", "not_checked"]
    uptime: float


app = FastAPI(title="Decision IQ Backend", version=APP_VERSION)

configure_logging()
add_middleware(app)
register_exception_handlers(app)
app.include_router(auth_router, prefix=settings.api_v1_prefix)


def get_uptime() -> float:
    return round(time.monotonic() - START_TIME, 2)


def build_health_response(
    *,
    status: Literal["healthy", "degraded", "unhealthy"],
    database: Literal["up", "down", "not_checked"],
) -> HealthResponse:
    return HealthResponse(
        status=status,
        environment=settings.environment.value,
        database=database,
        uptime=get_uptime(),
    )


@app.get("/health", response_model=HealthResponse)
def health(http_response: Response) -> HealthResponse:
    database_healthy = check_database_health()
    health_response = build_health_response(
        status="healthy" if database_healthy else "degraded",
        database="up" if database_healthy else "down",
    )
    if not database_healthy:
        http_response.status_code = 503
    return health_response


@app.get("/health/database", response_model=HealthResponse)
def database_health(http_response: Response) -> HealthResponse:
    database_healthy = check_database_health()
    health_response = build_health_response(
        status="healthy" if database_healthy else "unhealthy",
        database="up" if database_healthy else "down",
    )
    if not database_healthy:
        http_response.status_code = 503
    return health_response


@app.get("/health/application", response_model=HealthResponse)
def application_health() -> HealthResponse:
    return build_health_response(
        status="healthy",
        database="not_checked",
    )
