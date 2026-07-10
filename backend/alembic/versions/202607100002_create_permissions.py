"""create permissions table

Revision ID: 202607100002
Revises: 202607100001
Create Date: 2026-07-10 00:02:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "202607100002"
down_revision = "202607100001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "permissions",
        sa.Column("id", sa.Uuid(), primary_key=True, nullable=False),
        sa.Column("role_id", sa.Uuid(), nullable=False),
        sa.Column("resource", sa.String(length=128), nullable=False),
        sa.Column("action", sa.String(length=128), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("role_id", "resource", "action"),
    )
    op.create_index(op.f("ix_permissions_role_id"), "permissions", ["role_id"], unique=False)
    op.create_index(op.f("ix_permissions_resource"), "permissions", ["resource"], unique=False)
    op.create_index(op.f("ix_permissions_action"), "permissions", ["action"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_permissions_action"), table_name="permissions")
    op.drop_index(op.f("ix_permissions_resource"), table_name="permissions")
    op.drop_index(op.f("ix_permissions_role_id"), table_name="permissions")
    op.drop_table("permissions")
