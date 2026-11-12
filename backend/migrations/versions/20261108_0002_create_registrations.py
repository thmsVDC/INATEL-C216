"""Create event registrations.

Revision ID: 20261108_0002
Revises: 20261103_0001
Create Date: 2026-11-08
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261108_0002"
down_revision: str | Sequence[str] | None = "20261103_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "registrations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("participant_name", sa.String(length=120), nullable=False),
        sa.Column("participant_email", sa.String(length=254), nullable=False),
        sa.Column(
            "registered_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["event_id"], ["events.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "event_id",
            "participant_email",
            name="uq_registrations_event_email",
        ),
    )
    op.create_index(
        "ix_registrations_event_id",
        "registrations",
        ["event_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_registrations_event_id", table_name="registrations")
    op.drop_table("registrations")
