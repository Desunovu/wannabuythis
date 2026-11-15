"""make wishlist columns not null

Revision ID: 62abeb210c89
Revises: b7f1c2a9d4e0
Create Date: 2026-11-15 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "62abeb210c89"
down_revision: str | None = "b7f1c2a9d4e0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("wishlists", "name", existing_type=sa.String(), nullable=False)
    op.alter_column(
        "wishlists", "is_archived", existing_type=sa.Boolean(), nullable=False
    )
    op.alter_column(
        "wishlists", "is_public", existing_type=sa.Boolean(), nullable=False
    )
    op.alter_column(
        "wishlists", "created_at", existing_type=sa.DateTime(), nullable=False
    )
    op.alter_column("wishlist_items", "name", existing_type=sa.String(), nullable=False)
    op.alter_column(
        "wishlist_items", "quantity", existing_type=sa.Integer(), nullable=False
    )
    op.alter_column(
        "wishlist_items",
        "measurement_unit",
        existing_type=sa.Enum("PIECE", "METER", "KILOGRAM", name="measurementunit"),
        nullable=False,
    )
    op.alter_column(
        "wishlist_items",
        "priority",
        existing_type=sa.Enum("LOW", "MEDIUM", "HIGH", name="priority"),
        nullable=False,
    )
    op.alter_column(
        "wishlist_items", "is_purchased", existing_type=sa.Boolean(), nullable=False
    )


def downgrade() -> None:
    op.alter_column(
        "wishlist_items", "is_purchased", existing_type=sa.Boolean(), nullable=True
    )
    op.alter_column(
        "wishlist_items",
        "priority",
        existing_type=sa.Enum("LOW", "MEDIUM", "HIGH", name="priority"),
        nullable=True,
    )
    op.alter_column(
        "wishlist_items",
        "measurement_unit",
        existing_type=sa.Enum("PIECE", "METER", "KILOGRAM", name="measurementunit"),
        nullable=True,
    )
    op.alter_column(
        "wishlist_items", "quantity", existing_type=sa.Integer(), nullable=True
    )
    op.alter_column("wishlist_items", "name", existing_type=sa.String(), nullable=True)
    op.alter_column(
        "wishlists", "created_at", existing_type=sa.DateTime(), nullable=True
    )
    op.alter_column("wishlists", "is_public", existing_type=sa.Boolean(), nullable=True)
    op.alter_column(
        "wishlists", "is_archived", existing_type=sa.Boolean(), nullable=True
    )
    op.alter_column("wishlists", "name", existing_type=sa.String(), nullable=True)
