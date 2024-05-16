from src.shared_kernel.aggregates import AggregateRoot
from src.wishlist.domain.events import ItemAdded, ItemRemoved, ItemNotFound
from src.wishlist.domain.wishlist_item import WishlistItem


class Wishlist(AggregateRoot):
    def __init__(self, id: int, user_id: int, name: str):
        super().__init__(id)
        self.user_id = user_id
        self.name = name
        self.items = []

    def add_item(self, item: WishlistItem):
        self.items.append(item)
        self.add_event(ItemAdded(self.id, item.id))

    def remove_item(self, item_id: int):
        item = next((item for item in self.items if item.id == item_id), None)
        if item is None:
            self.add_event(ItemNotFound(self.id, item_id))
        else:
            self.items.remove(item)
            self.add_event(ItemRemoved(self.id, item_id))
