from dataclasses import dataclass
from uuid import UUID

from src.common.domain.aggregates import AggregateRoot
from src.common.domain.entities import Entity
from src.common.domain.value_objects import ValueObject
from src.wishlists.domain.events import (
    WishlistNameChanged,
    WishlistItemAdded,
    WishlistItemRemoved,
    WishlistItemMarkedAsPurchased,
    WishlistItemMarkedAsNotPurchased,
    WishlistUnarchived,
    WishlistArchived,
)


@dataclass
class MeasurementUnit(ValueObject):
    name: str


@dataclass
class Priority(ValueObject):
    value: int


class WishlistItem(Entity):
    def __init__(
        self,
        uuid: UUID,
        wishlist_uuid: UUID,
        name: str,
        quantity: int,
        measurement_unit: MeasurementUnit,
        priority: Priority,
    ):
        super().__init__()
        self.uuid = uuid
        self.wishlist_uuid = wishlist_uuid
        self.name = name
        self.quantity = quantity
        self.measurement_unit = measurement_unit
        self.priority = priority
        self.is_purchased = False


class Wishlist(AggregateRoot):
    def __init__(
        self, uuid: UUID, owner_username: str, name: str, items: list[WishlistItem]
    ):
        super().__init__()
        self.uuid = uuid
        self.owner_username = owner_username
        self.name = name
        self.items = items
        self.is_archived = False

    def change_name(self, name: str):
        self.name = name
        self.add_event(WishlistNameChanged(self.uuid, self.name))

    def archive(self):
        self.is_archived = True
        self.add_event(WishlistArchived(self.uuid))

    def unarchive(self):
        self.is_archived = False
        self.add_event(WishlistUnarchived(self.uuid))

    def add_item(self, item: WishlistItem):
        self.items.append(item)
        self.add_event(
            WishlistItemAdded(
                item_uuid=item.uuid,
                wishlist_uuid=self.uuid,
                name=item.name,
                quantity=item.quantity,
                measurement_unit=item.measurement_unit.name,
                priority=item.priority.value,
            )
        )

    def remove_item(self, item_uuid: UUID):
        self.items = [item for item in self.items if item.uuid != item_uuid]
        self.add_event(
            WishlistItemRemoved(item_uuid=item_uuid, wishlist_uuid=self.uuid)
        )

    def find_item(self, item_uuid: UUID):
        return next((item for item in self.items if item.uuid == item_uuid), None)

    def set_item_status(self, item_uuid: UUID, is_purchased: bool):
        item = self.find_item(item_uuid)
        if item is None:
            raise ValueError(
                f"Item with UUID {item_uuid} not found in wishlist {self.uuid}"
            )
        item.is_purchased = is_purchased
        event_class = (
            WishlistItemMarkedAsPurchased
            if is_purchased
            else WishlistItemMarkedAsNotPurchased
        )
        self.add_event(event_class(item_uuid=item_uuid, wishlist_uuid=self.uuid))
