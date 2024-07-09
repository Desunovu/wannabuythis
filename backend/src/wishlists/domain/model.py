import enum
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from src.common.domain.aggregates import AggregateRoot
from src.common.domain.entities import Entity
from src.common.service.exceptions import WishlistItemNotFound
from src.wishlists.domain.events import (
    WishlistArchived,
    WishlistCreated,
    WishlistItemAdded,
    WishlistItemMarkedAsNotPurchased,
    WishlistItemMarkedAsPurchased,
    WishlistItemRemoved,
    WishlistNameChanged,
    WishlistUnarchived,
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
        self._add_event(WishlistCreated(uuid=self.uuid, name=self.name))

    def change_name(self, name: str):
        self.name = name
        self._add_event(WishlistNameChanged(self.uuid, self.name))

    def archive(self):
        self.is_archived = True
        self._add_event(WishlistArchived(self.uuid))

    def unarchive(self):
        self.is_archived = False
        self._add_event(WishlistUnarchived(self.uuid))

    def add_item(self, item: WishlistItem):
        self.items.append(item)
        self._add_event(
            WishlistItemAdded(
                item_uuid=item.uuid,
                wishlist_uuid=self.uuid,
                name=item.name,
                quantity=item.quantity,
                measurement_unit=item.measurement_unit.name,
                priority=item.priority.value,
            )
        )

    def __find_item(self, item_uuid: UUID):
        try:
            return next(item for item in self.items if item.uuid == item_uuid)
        except StopIteration:
            raise WishlistItemNotFound(item_uuid)

    def remove_item(self, item_uuid: UUID):
        item = self.__find_item(item_uuid)
        self.items.remove(item)
        self._add_event(
            WishlistItemRemoved(item_uuid=item_uuid, wishlist_uuid=self.uuid)
        )

    def set_item_status(self, item_uuid: UUID, is_purchased: bool):
        item = self.__find_item(item_uuid)
        item.is_purchased = is_purchased
        event = (
            WishlistItemMarkedAsPurchased(item_uuid=item_uuid, wishlist_uuid=self.uuid)
            if is_purchased
            else WishlistItemMarkedAsNotPurchased(
                item_uuid=item_uuid, wishlist_uuid=self.uuid
            )
        )
        self._add_event(event)
