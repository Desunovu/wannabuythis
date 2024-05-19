from dataclasses import dataclass

from src.domain.shared_kernel.commands import Command


@dataclass
class CreateWishlist(Command):
    username: str
    name: str


@dataclass
class ChangeWishlistName(Command):
    uuid: str
    name: str


@dataclass
class AddWishlistItem(Command):
    uuid: str
    name: str
    quantity: int
    measurement_unit: str
    priority: int


@dataclass
class RemoveWishlistItem(Command):
    uuid: str
    item_uuid: str
