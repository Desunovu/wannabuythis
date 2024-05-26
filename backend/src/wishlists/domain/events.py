from dataclasses import dataclass
from typing import Protocol
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
class WishlistArchived(DomainEvent):
    uuid: UUID


@dataclass
class WishlistUnarchived(DomainEvent):
    uuid: UUID


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


@dataclass
class WishlistItemMarkedAsPurchased(DomainEvent):
    item_uuid: UUID
    wishlist_uuid: UUID


@dataclass
class WishlistItemMarkedAsNotPurchased(DomainEvent):
    item_uuid: UUID
    wishlist_uuid: UUID
