import abc
from uuid import UUID

from src.wishlists.domain.model import Wishlist


class WishlistRepository(abc.ABC):
    def __init__(self):
        self.seen: set[Wishlist] = set()

    def get(self, uuid: UUID) -> Wishlist | None:
        wishlist = self._get(uuid)
        if wishlist:
            self.seen.add(wishlist)
        return wishlist

    def list_all(self) -> list[Wishlist]:
        wishlists = self._list_all()
        self.seen.update(wishlists)
        return wishlists

    def list_owned_by(self, username: str) -> list[Wishlist]:
        wishlists = self._list_owned_by(username)
        self.seen.update(wishlists)
        return wishlists

    def add(self, wishlist: Wishlist):
        self._add(wishlist)
        self.seen.add(wishlist)

    @abc.abstractmethod
    def _get(self, uuid: UUID) -> Wishlist | None: ...

    @abc.abstractmethod
    def _list_all(self) -> list[Wishlist]: ...

    @abc.abstractmethod
    def _list_owned_by(self, username: str) -> list[Wishlist]: ...

    @abc.abstractmethod
    def _add(self, user: Wishlist): ...
