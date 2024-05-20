from dataclasses import dataclass

from src.common.domain.commands import Command


@dataclass
class CreateWishlist(Command):
    owner_username: str
    name: str


@dataclass
class ChangeWishlistName(Command):
    uuid: str
    new_name: str


@dataclass
class AddWishlistItem(Command):
    wishlist_uuid: str
    name: str
    quantity: int
    measurement_unit: str
    priority: int


@dataclass
class RemoveWishlistItem(Command):
    wishlist_uuid: str
    item_uuid: str
