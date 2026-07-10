from __future__ import annotations

from enum import Enum

from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin
from app.models.associations import user_roles


class RoleName(str, Enum):
    """Supported application roles."""

    CITIZEN = "Citizen"
    COMMUNITY = "Community"
    ORGANIZATION = "Organization"
    ANALYST = "Analyst"
    ADMIN = "Admin"


class Role(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    """Role assigned to users through a many-to-many relationship."""

    __tablename__ = "roles"

    name: Mapped[RoleName] = mapped_column(
        SAEnum(
            RoleName,
            name="role_name",
            native_enum=False,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        unique=True,
        index=True,
        nullable=False,
    )
    users: Mapped[list["User"]] = relationship(
        secondary=user_roles,
        back_populates="roles",
        lazy="selectin",
    )
    permissions: Mapped[list["Permission"]] = relationship(
        back_populates="role",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
