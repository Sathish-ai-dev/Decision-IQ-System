from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, TimestampMixin, UUIDMixin


class Permission(UUIDMixin, TimestampMixin, Base):
    """Permission granted to a role for a resource and action."""

    __tablename__ = "permissions"
    __table_args__ = (
        UniqueConstraint("role_id", "resource", "action"),
    )

    role_id: Mapped[UUID] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    resource: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    role: Mapped["Role"] = relationship(back_populates="permissions", lazy="selectin")
