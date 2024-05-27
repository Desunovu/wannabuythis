from typing import Optional

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    TypeDecorator,
    Dialect,
    Uuid,
    Boolean,
)
from sqlalchemy.orm import registry, relationship

from src.roles.domain import model as role_domain_model
from src.users.domain import model as user_domain_model
from src.wishlists.domain import model as wishlist_domain_model

mapper_registry = registry()


class MeasurementUnitType(TypeDecorator):
    impl = String

    def process_bind_param(
        self, measurement_unit: wishlist_domain_model.MeasurementUnit, dialect: Dialect
    ) -> str:
        return measurement_unit.name

    def process_result_value(
        self, value: Optional[str], dialect: Dialect
    ) -> Optional[wishlist_domain_model.MeasurementUnit]:
        if value is not None:
            return wishlist_domain_model.MeasurementUnit(name=value)


class PriorityType(TypeDecorator):
    impl = Integer

    def process_bind_param(
        self, priority: wishlist_domain_model.Priority, dialect: Dialect
    ) -> int:
        return priority.value

    def process_result_value(
        self, value: Optional[int], dialect: Dialect
    ) -> Optional[wishlist_domain_model.Priority]:
        if value is not None:
            return wishlist_domain_model.Priority(value=value)


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
    Column("measurement_unit", MeasurementUnitType),
    Column("priority", PriorityType),
    Column("is_purchased", Boolean),
)

measurement_units = Table(
    "measurement_units",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
)

priorities = Table(
    "priorities",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("value", Integer, unique=True),
)


def start_mappers():
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
    mapper_registry.map_imperatively(
        wishlist_domain_model.MeasurementUnit, measurement_units
    )
    mapper_registry.map_imperatively(wishlist_domain_model.Priority, priorities)

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
