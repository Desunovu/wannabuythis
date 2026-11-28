"""add wishlist items wishlist_uuid index

Revision ID: a3f5c9d1b7e2
Revises: 62abeb210c89
Create Date: 2026-11-15 12:30:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a3f5c9d1b7e2"
down_revision: str | None = "62abeb210c89"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_index(
        "ix_wishlist_items_wishlist_uuid", "wishlist_items", ["wishlist_uuid"]
    )


def downgrade() -> None:
    op.drop_index("ix_wishlist_items_wishlist_uuid", table_name="wishlist_items")
