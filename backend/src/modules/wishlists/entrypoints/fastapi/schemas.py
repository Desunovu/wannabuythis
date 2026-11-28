from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from src.config import settings
from src.modules.wishlists.domain.model import MeasurementUnit, Priority

WishlistName = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=settings.wishlists_name_max_length,
    ),
]
WishlistItemName = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=settings.wishlists_item_name_max_length,
    ),
]
WishlistItemQuantity = Annotated[
    int, Field(gt=0, le=settings.wishlists_item_quantity_max)
]


class WishlistItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    wishlist_uuid: UUID
    name: str
    quantity: int
    measurement_unit: MeasurementUnit
    priority: Priority
    is_purchased: bool
    created_at: datetime


class WishlistResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    owner_username: str
    name: str
    items: list[WishlistItemResponse]
    is_archived: bool
    is_public: bool
    created_at: datetime


class CreateWishlistRequest(BaseModel):
    wishlist_name: WishlistName
    is_public: bool


class ChangeWishlistNameRequest(BaseModel):
    new_name: WishlistName


class ChangeWishlistVisibilityRequest(BaseModel):
    is_public: bool


class AddWishlistItemRequest(BaseModel):
    name: WishlistItemName
    quantity: WishlistItemQuantity
    measurement_unit: MeasurementUnit
    priority: Priority


class RemoveWishlistItemRequest(BaseModel):
    item_uuid: UUID


class SetWishlistItemStatusRequest(BaseModel):
    item_uuid: UUID
