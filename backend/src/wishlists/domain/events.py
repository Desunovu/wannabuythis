from dataclasses import dataclass

from src.common.domain.events import DomainEvent


@dataclass
class WishlistCreated(DomainEvent):
    uuid: str
    name: str


@dataclass
class WishlistNameChanged(DomainEvent):
    uuid: str
    name: str


@dataclass
class WishlistItemAdded(DomainEvent):
    item_uuid: str
    wishlist_uuid: str
    name: str
    quantity: int
    measurement_unit: str
    priority: int


@dataclass
class WishlistItemRemoved(DomainEvent):
    item_uuid: str
    wishlist_uuid: str
