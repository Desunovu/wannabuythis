import enum
from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import UUID

from src.common.domain.aggregates import AggregateRoot
from src.common.domain.entities import Entity
from src.common.service.exceptions import WishlistItemNotFound
from src.wishlists.domain.events import (
    WishlistNameChanged,
    WishlistItemAdded,
    WishlistItemRemoved,
    WishlistItemMarkedAsPurchased,
    WishlistItemMarkedAsNotPurchased,
    WishlistUnarchived,
    WishlistArchived,
    WishlistCreated,
)


class MeasurementUnit(str, enum.Enum):
    PIECE = "piece"
    METER = "meter"
    KILOGRAM = "kg."


class Priority(int, enum.Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass(kw_only=True)
class WishlistItem(Entity):
    uuid: UUID
    wishlist_uuid: UUID
    name: str
    quantity: int
    measurement_unit: MeasurementUnit
    priority: Priority
    is_purchased: bool = field(default=False)


@dataclass(kw_only=True, unsafe_hash=True)
class Wishlist(AggregateRoot):
    uuid: UUID
    owner_username: str
    name: str
    items: list[WishlistItem] = field(default_factory=list, compare=False)
    is_archived: bool = field(default=False)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self):
        self.add_event(WishlistCreated(uuid=self.uuid, name=self.name))

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

    def find_item(self, item_uuid: UUID):
        return next((item for item in self.items if item.uuid == item_uuid), None)

    def remove_item(self, item_uuid: UUID):
        item = self.find_item(item_uuid)
        if item is None:
            raise WishlistItemNotFound(item_uuid)
        self.items.remove(item)
        self.add_event(
            WishlistItemRemoved(item_uuid=item_uuid, wishlist_uuid=self.uuid)
        )

    def set_item_status(self, item_uuid: UUID, is_purchased: bool):
        item = self.find_item(item_uuid)
        if item is None:
            raise WishlistItemNotFound(item_uuid)
        item.is_purchased = is_purchased
        event = (
            WishlistItemMarkedAsPurchased(item_uuid=item_uuid, wishlist_uuid=self.uuid)
            if is_purchased
            else WishlistItemMarkedAsNotPurchased(
                item_uuid=item_uuid, wishlist_uuid=self.uuid
            )
        )
        self.add_event(event)
