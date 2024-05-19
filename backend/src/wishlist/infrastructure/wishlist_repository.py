import abc

from src.wishlist.domain.wishlist import Wishlist


class WishlistRepository(abc.ABC):
    def __init__(self):
        self.seen: set[Wishlist] = set()

    def get(self, wishlist_id: int) -> Wishlist | None:
        wishlist = self._get(wishlist_id)
        if wishlist:
            self.seen.add(wishlist)
        return wishlist

    def add(self, wishlist: Wishlist):
        self._add(wishlist)
        self.seen.add(wishlist)

    @abc.abstractmethod
    def _get(self, user_id: int) -> Wishlist | None: ...

    @abc.abstractmethod
    def _add(self, user: Wishlist): ...
