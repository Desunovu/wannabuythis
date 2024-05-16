from src.shared_kernel.events import DomainEvent


class ItemAdded(DomainEvent):
    def __init__(self, wishlist_id: int, item_id: int):
        self.wishlist_id = wishlist_id
        self.item_id = item_id


class ItemRemoved(DomainEvent):
    def __init__(self, wishlist_id: int, item_id: int):
        self.wishlist_id = wishlist_id
        self.item_id = item_id


class ItemNotFound(DomainEvent):
    def __init__(self, wishlist_id: int, item_id: int):
        self.wishlist_id = wishlist_id
        self.item_id = item_id
