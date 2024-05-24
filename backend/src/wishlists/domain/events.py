from dataclasses import dataclass
from uuid import UUID

from src.common.domain.events import DomainEvent


@dataclass
class WishlistCreated(DomainEvent):
    uuid: UUID
    name: str


@dataclass
class WishlistNameChanged(DomainEvent):
    uuid: UUID
    name: str


@dataclass
class WishlistItemAdded(DomainEvent):
    item_uuid: UUID
    wishlist_uuid: UUID
    name: str
    quantity: int
    measurement_unit: str
    priority: int


@dataclass
class WishlistItemRemoved(DomainEvent):
    item_uuid: UUID
    wishlist_uuid: UUID
