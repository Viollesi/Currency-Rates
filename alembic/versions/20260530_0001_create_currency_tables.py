"""create currency tables

Revision ID: 20260530_0001
Revises:
Create Date: 2026-05-30
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260530_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create currency rate tables."""
    op.create_table(
        "currency_rates_raw",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("rate_date", sa.Date(), nullable=False),
        sa.Column("raw_xml", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_currency_rates_raw_id"), "currency_rates_raw", ["id"], unique=False)
    op.create_index(
        op.f("ix_currency_rates_raw_rate_date"),
        "currency_rates_raw",
        ["rate_date"],
        unique=False,
    )

    op.create_table(
        "currency_rates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=3), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("nominal", sa.Integer(), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("rate_date", sa.Date(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_currency_rates_code"), "currency_rates", ["code"], unique=False)
    op.create_index(op.f("ix_currency_rates_id"), "currency_rates", ["id"], unique=False)
    op.create_index(
        op.f("ix_currency_rates_rate_date"),
        "currency_rates",
        ["rate_date"],
        unique=False,
    )


def downgrade() -> None:
    """Drop currency rate tables."""
    op.drop_index(op.f("ix_currency_rates_rate_date"), table_name="currency_rates")
    op.drop_index(op.f("ix_currency_rates_id"), table_name="currency_rates")
    op.drop_index(op.f("ix_currency_rates_code"), table_name="currency_rates")
    op.drop_table("currency_rates")

    op.drop_index(op.f("ix_currency_rates_raw_rate_date"), table_name="currency_rates_raw")
    op.drop_index(op.f("ix_currency_rates_raw_id"), table_name="currency_rates_raw")
    op.drop_table("currency_rates_raw")
