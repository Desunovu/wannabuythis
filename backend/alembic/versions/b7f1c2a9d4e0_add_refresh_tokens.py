"""add refresh tokens

Revision ID: b7f1c2a9d4e0
Revises: d639cd7c411e
Create Date: 2026-10-11 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b7f1c2a9d4e0"
down_revision: str | None = "d639cd7c411e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "refresh_tokens",
        sa.Column("token_hash", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["username"], ["users.username"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("token_hash"),
    )
    op.create_index("ix_refresh_tokens_username", "refresh_tokens", ["username"])


def downgrade() -> None:
    op.drop_index("ix_refresh_tokens_username", table_name="refresh_tokens")
    op.drop_table("refresh_tokens")
