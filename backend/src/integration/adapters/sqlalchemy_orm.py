from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    Uuid,
    Boolean,
    event,
    Enum,
)
from sqlalchemy.orm import registry, relationship

from src.users.domain import model as user_domain_model
from src.wishlists.domain import model as wishlist_domain_model

mapper_registry = registry()

users = Table(
    "users",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True),
    Column("email", String, unique=True),
    Column("password_hash", String),
    Column("is_active", Boolean),
    Column("is_superuser", Boolean, default=False),
)

wishlists = Table(
    "wishlists",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("uuid", Uuid, unique=True),
    Column("owner_username", String, ForeignKey("users.username"), nullable=False),
    Column("name", String),
    Column("is_archived", Boolean),
)

wishlist_items = Table(
    "wishlist_items",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("uuid", Uuid, unique=True),
    Column("wishlist_uuid", Uuid, ForeignKey("wishlists.uuid"), nullable=False),
    Column("name", String),
    Column("quantity", Integer),
    Column("measurement_unit", Enum(wishlist_domain_model.MeasurementUnit)),
    Column("priority", Enum(wishlist_domain_model.Priority)),
    Column("is_purchased", Boolean),
)


def start_sqlalchemy_mappers():
    # Users context
    mapper_registry.map_imperatively(user_domain_model.User, users)

    # Wishlists context
    mapper_registry.map_imperatively(
        wishlist_domain_model.Wishlist,
        wishlists,
        properties={
            "items": relationship(
                wishlist_domain_model.WishlistItem,
                order_by=wishlist_items.c.id,
                lazy="dynamic",
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


def add_events_field_listener(aggregate):
    @event.listens_for(aggregate, "load")
    def add_events_field(target, context):
        target.events = []
