from dataclasses import dataclass
from uuid import UUID

from src.common.domain.commands import Command


@dataclass
class CreateWishlist(Command):
    owner_username: str
    name: str


@dataclass
class ChangeWishlistName(Command):
    uuid: UUID
    new_name: str


@dataclass
class ArchiveWishlist(Command):
    uuid: UUID


@dataclass
class UnarchiveWishlist(Command):
    uuid: UUID


@dataclass
class AddWishlistItem(Command):
    wishlist_uuid: UUID
    name: str
    quantity: int
    measurement_unit: str
    priority: int


@dataclass
class RemoveWishlistItem(Command):
    wishlist_uuid: UUID
    item_uuid: UUID


@dataclass
class SetWishlistItemStatus(Command):
    wishlist_uuid: UUID
    item_uuid: UUID
    is_purchased: bool
