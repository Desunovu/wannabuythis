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
)
from sqlalchemy.orm import registry, relationship

from src.users.domain.user import User
from src.wishlists.domain.wishlist import Wishlist
from src.wishlists.domain.wishlist_item import WishlistItem, MeasurementUnit, Priority

mapper_registry = registry()


class MeasurementUnitType(TypeDecorator):
    impl = String

    def process_bind_param(
        self, measurement_unit: MeasurementUnit, dialect: Dialect
    ) -> str:
        return measurement_unit.name

    def process_result_value(
        self, value: Optional[str], dialect: Dialect
    ) -> Optional[MeasurementUnit]:
        if value is not None:
            return MeasurementUnit(name=value)


class PriorityType(TypeDecorator):
    impl = Integer

    def process_bind_param(self, priority: Priority, dialect: Dialect) -> int:
        return priority.value

    def process_result_value(
        self, value: Optional[int], dialect: Dialect
    ) -> Optional[Priority]:
        if value is not None:
            return Priority(value=value)


users_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True),
    Column("email", String, unique=True),
    Column("password_hash", String),
)

wishlists_table = Table(
    "wishlists",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("uuid", Uuid, unique=True),
    Column("owner_username", String, ForeignKey("users.username"), nullable=False),
    Column("name", String),
)

wishlist_items_table = Table(
    "wishlist_items",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("uuid", Uuid, unique=True),
    Column("wishlist_uuid", Uuid, ForeignKey("wishlists.uuid"), nullable=False),
    Column("name", String),
    Column("quantity", Integer),
    Column("measurement_unit", MeasurementUnitType),
    Column("priority", PriorityType),
)


def start_mappers():
    mapper_registry.map_imperatively(User, users_table)
    mapper_registry.map_imperatively(
        Wishlist,
        wishlists_table,
        properties={
            "items": relationship(
                WishlistItem, order_by=wishlist_items_table.c.id, lazy="dynamic"
            )
        },
    )
    mapper_registry.map_imperatively(WishlistItem, wishlist_items_table)
