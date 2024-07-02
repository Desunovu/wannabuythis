from dataclasses import asdict
from uuid import UUID

from pydantic import BaseModel

from src.wishlists.domain.model import MeasurementUnit, Priority


class WishlistItemResponse(BaseModel):
    uuid: UUID
    wishlist_uuid: UUID
    name: str
    quantity: int
    measurement_unit: MeasurementUnit
    priority: Priority
    is_purchased: bool

    @classmethod
    def from_dataclass(cls, wishlist_item):
        return cls(**asdict(wishlist_item))


class WishlistResponse(BaseModel):
    uuid: UUID
    owner_username: str
    name: str
    items: list[WishlistItemResponse]
    is_archived: bool

    @classmethod
    def from_dataclass(cls, wishlist):
        return cls(
            uuid=wishlist.uuid,
            owner_username=wishlist.owner_username,
            name=wishlist.name,
            items=[
                WishlistItemResponse.from_dataclass(item) for item in wishlist.items
            ],
            is_archived=wishlist.is_archived,
        )
