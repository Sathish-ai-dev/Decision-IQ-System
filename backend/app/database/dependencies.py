from __future__ import annotations

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database.session import get_session


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that provides a database session."""

    yield from get_session()


