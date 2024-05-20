from src.domain.shared_kernel.aggregates import AggregateRoot
from src.domain.wishlist.events import (
    WishlistNameChanged,
    WishlistItemAdded,
    WishlistItemRemoved,
)
from src.domain.wishlist.wishlist_item import WishlistItem


# TODO: Add WORKSPACE Aggregate???
class Wishlist(AggregateRoot):
    def __init__(
        self, uuid: str, owner_username: str, name: str, items: list[WishlistItem]
    ):
        super().__init__()
        self.uuid = uuid
        self.owner_username = owner_username
        self.name = name
        self.items = items

    def change_name(self, name: str):
        self.name = name
        self.add_event(WishlistNameChanged(self.uuid, self.name))

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

    def remove_item(self, item_uuid: str):
        self.items = [item for item in self.items if item.uuid != item_uuid]
        self.add_event(
            WishlistItemRemoved(item_uuid=item_uuid, wishlist_uuid=self.uuid)
        )
