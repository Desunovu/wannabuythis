from src.shared_kernel.aggregates import AggregateRoot
from src.user.domain.events import WishlistAdded, WishlistRemoved, WishlistNotFound
from src.wishlist.domain.wishlist import Wishlist


class User(AggregateRoot):
    def __init__(self, id: int, name: str, email: str):
        super().__init__(id)
        self.name = name
        self.email = email
        self.wishlists = []

    def add_wishlist(self, wishlist: Wishlist):
        self.wishlists.append(wishlist)
        self.add_event(WishlistAdded(self.id, wishlist.id))

    def remove_wishlist(self, wishlist_id: int):
        wishlist = next((wl for wl in self.wishlists if wl.id == wishlist_id), None)
        if wishlist is None:
            self.add_event(WishlistNotFound(self.id, wishlist_id))
        else:
            self.wishlists.remove(wishlist)
            self.add_event(WishlistRemoved(self.id, wishlist_id))
