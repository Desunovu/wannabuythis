"""remove usage of id primary key in tables

Revision ID: 0ca315882232
Revises: 6aebf7eb6ed4
Create Date: 2024-07-08 15:07:39.403356

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0ca315882232"
down_revision: Union[str, None] = "6aebf7eb6ed4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Users table
    op.execute("ALTER TABLE users DROP CONSTRAINT users_pkey")
    op.execute("ALTER TABLE users ADD PRIMARY KEY (username)")
    op.execute("ALTER TABLE users DROP COLUMN id")

    # Wishlists table
    op.execute("ALTER TABLE wishlists DROP CONSTRAINT wishlists_pkey")
    op.execute("ALTER TABLE wishlists ADD PRIMARY KEY (uuid)")
    op.execute("ALTER TABLE wishlists DROP COLUMN id")

    # Wishlist items table
    op.execute("ALTER TABLE wishlist_items DROP CONSTRAINT wishlist_items_pkey")
    op.execute("ALTER TABLE wishlist_items ADD PRIMARY KEY (uuid)")
    op.execute("ALTER TABLE wishlist_items DROP COLUMN id")


def downgrade():
    # Users table
    op.execute("ALTER TABLE users ADD COLUMN id SERIAL PRIMARY KEY")
    op.execute("ALTER TABLE users DROP CONSTRAINT users_pkey")
    op.execute("ALTER TABLE users ADD CONSTRAINT users_pkey PRIMARY KEY (id)")
    op.execute("ALTER TABLE users ADD UNIQUE (username)")

    # Wishlists table
    op.execute("ALTER TABLE wishlists ADD COLUMN id SERIAL PRIMARY KEY")
    op.execute("ALTER TABLE wishlists DROP CONSTRAINT wishlists_pkey")
    op.execute("ALTER TABLE wishlists ADD CONSTRAINT wishlists_pkey PRIMARY KEY (id)")
    op.execute("ALTER TABLE wishlists ADD UNIQUE (uuid)")

    # Wishlist items table
    op.execute("ALTER TABLE wishlist_items ADD COLUMN id SERIAL PRIMARY KEY")
    op.execute("ALTER TABLE wishlist_items DROP CONSTRAINT wishlist_items_pkey")
    op.execute(
        "ALTER TABLE wishlist_items ADD CONSTRAINT wishlist_items_pkey PRIMARY KEY (id)"
    )
    op.execute("ALTER TABLE wishlist_items ADD UNIQUE (uuid)")
