from dataclasses import dataclass
from uuid import UUID

from src.common.domain.commands import Command


@dataclass(frozen=True)
class CreateWishlist(Command):
    owner_username: str
    name: str


@dataclass(frozen=True)
class ChangeWishlistName(Command):
    uuid: UUID
    new_name: str


@dataclass(frozen=True)
class ArchiveWishlist(Command):
    uuid: UUID


@dataclass(frozen=True)
class UnarchiveWishlist(Command):
    uuid: UUID


@dataclass(frozen=True)
class AddWishlistItem(Command):
    wishlist_uuid: UUID
    name: str
    quantity: int
    measurement_unit: str
    priority: int


@dataclass(frozen=True)
class RemoveWishlistItem(Command):
    wishlist_uuid: UUID
    item_uuid: UUID


@dataclass(frozen=True)
class SetWishlistItemStatus(Command):
    wishlist_uuid: UUID
    item_uuid: UUID
    is_purchased: bool
