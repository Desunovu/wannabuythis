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

from src.roles.domain import model as role_domain_model
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
)

roles = Table(
    "roles",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
)

user_roles = Table(
    "user_roles",
    mapper_registry.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)

permissions = Table(
    "permissions",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
)

role_permissions = Table(
    "role_permissions",
    mapper_registry.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),
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
    mapper_registry.map_imperatively(
        user_domain_model.User,
        users,
        properties={
            "roles": relationship(user_domain_model.Role, secondary=user_roles)
        },
    )
    mapper_registry.map_imperatively(
        user_domain_model.Role,
        roles,
        properties={
            "permissions": relationship(
                user_domain_model.Permission, secondary=role_permissions, viewonly=True
            )
        },
    )
    mapper_registry.map_imperatively(user_domain_model.Permission, permissions)

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

    # Roles context
    mapper_registry.map_imperatively(
        role_domain_model.Role,
        roles,
        properties={
            "permissions": relationship(
                role_domain_model.Permission,
                secondary=role_permissions,
                backref="roles",
            )
        },
    )
    mapper_registry.map_imperatively(role_domain_model.Permission, permissions)

    # Add events field to loaded aggregates
    aggregates = [
        user_domain_model.User,
        wishlist_domain_model.Wishlist,
        role_domain_model.Role,
    ]
    for aggregate in aggregates:
        add_events_field_listener(aggregate)


def add_events_field_listener(aggregate):
    @event.listens_for(aggregate, "load")
    def add_events_field(target, context):
        target.events = []
