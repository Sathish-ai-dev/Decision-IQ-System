from __future__ import annotations

from functools import lru_cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.pool import StaticPool

from app.core.config import settings


def _build_engine_kwargs(database_url: str) -> dict[str, object]:
    engine_kwargs: dict[str, object] = {
        "pool_pre_ping": True,
    }

    if database_url.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}
        if database_url.endswith(":memory:"):
            engine_kwargs["poolclass"] = StaticPool

    return engine_kwargs


def create_engine_from_settings(database_url: str | None = None) -> Engine:
    """Create a SQLAlchemy engine for the configured database URL."""

    resolved_url = database_url or settings.database_url
    if not resolved_url:
        raise ValueError("DATABASE_URL is not configured.")

    return create_engine(resolved_url, **_build_engine_kwargs(resolved_url))


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    return create_engine_from_settings()


engine = get_engine()


