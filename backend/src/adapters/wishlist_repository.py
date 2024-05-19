import abc

from src.domain.wishlist.wishlist import Wishlist


class WishlistRepository(abc.ABC):
    def __init__(self):
        self.seen: set[Wishlist] = set()

    def get(self, uuid: str) -> Wishlist | None:
        wishlist = self._get(uuid)
        if wishlist:
            self.seen.add(wishlist)
        return wishlist

    def add(self, wishlist: Wishlist):
        self._add(wishlist)
        self.seen.add(wishlist)

    @abc.abstractmethod
    def _get(self, uuid: str) -> Wishlist | None: ...

    @abc.abstractmethod
    def _add(self, user: Wishlist): ...
