"""Create the initial events table.

Revision ID: 20261103_0001
Revises:
Create Date: 2026-11-03
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261103_0001"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=60), nullable=False),
        sa.Column("location", sa.String(length=150), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint("capacity > 0", name="ck_events_capacity_positive"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_events_starts_at", "events", ["starts_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_events_starts_at", table_name="events")
    op.drop_table("events")
