from src.shared_kernel.domain.aggregates import AggregateRoot
from src.wishlist.domain.events import (
    WishlistNameChanged,
    WishlistItemAdded,
    WishlistItemRemoved,
)
from src.wishlist.domain.wishlist_item import WishlistItem


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
        self.add_event(WishlistItemAdded(item.uuid, item.name))

    def remove_item(self, item_uuid: str):
        self.items = [item for item in self.items if item.uuid != item_uuid]
        self.add_event(WishlistItemRemoved(item_uuid))
