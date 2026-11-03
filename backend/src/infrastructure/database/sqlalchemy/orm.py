import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    TypeDecorator,
    Uuid,
    event,
)
from sqlalchemy.orm import registry, relationship

from src.modules.users.domain import model as user_domain_model
from src.modules.wishlists.domain import model as wishlist_domain_model

mapper_registry = registry()


class UTCDateTime(TypeDecorator):
    """Store datetimes as UTC and restore tzinfo dropped by some backends (SQLite)."""

    impl = DateTime(timezone=True)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=datetime.UTC)
        return value.astimezone(datetime.UTC)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=datetime.UTC)
        return value.astimezone(datetime.UTC)


users = Table(
    "users",
    mapper_registry.metadata,
    Column("username", String, primary_key=True),
    Column("email", String, unique=True),
    Column("password_hash", String),
    Column("is_active", Boolean),
    Column("is_superuser", Boolean, default=False),
)

refresh_tokens = Table(
    "refresh_tokens",
    mapper_registry.metadata,
    Column("token_hash", String, primary_key=True),
    Column(
        "username",
        String,
        ForeignKey("users.username", ondelete="CASCADE"),
        nullable=False,
        index=True,
    ),
    Column("created_at", UTCDateTime, nullable=False),
    Column("expires_at", UTCDateTime, nullable=False),
    Column("revoked_at", UTCDateTime, nullable=True),
)


wishlists = Table(
    "wishlists",
    mapper_registry.metadata,
    Column("uuid", Uuid, primary_key=True),
    Column(
        "owner_username",
        String,
        ForeignKey("users.username", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("name", String),
    Column("is_archived", Boolean),
    Column("is_public", Boolean),
    Column("created_at", DateTime),  # TODO: use UTCDateTime for consistency
)

wishlist_items = Table(
    "wishlist_items",
    mapper_registry.metadata,
    Column("uuid", Uuid, primary_key=True),
    Column(
        "wishlist_uuid",
        Uuid,
        ForeignKey("wishlists.uuid", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("name", String),
    Column("quantity", Integer),
    Column("measurement_unit", Enum(wishlist_domain_model.MeasurementUnit)),
    Column("priority", Enum(wishlist_domain_model.Priority)),
    Column("is_purchased", Boolean),
)


def add_events_field_listener(aggregate):
    @event.listens_for(aggregate, "load")
    def add_events_field(target, context):
        target.events = []


def start_sqlalchemy_mappers():
    if mapper_registry.mappers:
        return
    # Users context
    mapper_registry.map_imperatively(user_domain_model.User, users)

    # Wishlists context
    mapper_registry.map_imperatively(
        wishlist_domain_model.Wishlist,
        wishlists,
        properties={
            "items": relationship(
                wishlist_domain_model.WishlistItem,
                order_by=wishlist_items.c.uuid,
                lazy="dynamic",
                cascade="all, delete-orphan",
            )
        },
    )
    mapper_registry.map_imperatively(wishlist_domain_model.WishlistItem, wishlist_items)

    # Add events field to loaded aggregates
    aggregates = [
        user_domain_model.User,
        wishlist_domain_model.Wishlist,
    ]
    for aggregate in aggregates:
        add_events_field_listener(aggregate)
