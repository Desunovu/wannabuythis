from dataclasses import dataclass


@dataclass
class CreateWishlist:
    username: str
    name: str


@dataclass
class ChangeWishlistName:
    uuid: str
    name: str


@dataclass
class AddWishlistItem:
    uuid: str
    name: str
    quantity: int
    measurement_unit: str
    priority: int


@dataclass
class RemoveWishlistItem:
    uuid: str
    item_uuid: str
