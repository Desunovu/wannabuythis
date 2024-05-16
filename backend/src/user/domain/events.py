from src.shared_kernel.events import DomainEvent


class WishlistAdded(DomainEvent):
    def __init__(self, user_id: int, wishlist_id: int):
        self.user_id = user_id
        self.wishlist_id = wishlist_id


class WishlistRemoved(DomainEvent):
    def __init__(self, user_id: int, wishlist_id: int):
        self.user_id = user_id
        self.wishlist_id = wishlist_id


class WishlistNotFound(DomainEvent):
    def __init__(self, user_id: int, wishlist_id: int):
        self.user_id = user_id
        self.wishlist_id = wishlist_id
