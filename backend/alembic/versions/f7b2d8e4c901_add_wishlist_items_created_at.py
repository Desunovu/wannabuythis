"""add wishlist items created_at

Revision ID: f7b2d8e4c901
Revises: a3f5c9d1b7e2
Create Date: 2026-11-15 13:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f7b2d8e4c901"
down_revision: str | None = "a3f5c9d1b7e2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "wishlist_items",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("wishlist_items", "created_at")
