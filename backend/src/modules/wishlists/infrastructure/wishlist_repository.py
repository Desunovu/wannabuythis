import abc
from uuid import UUID

from src.modules.wishlists.domain.model import Wishlist
from src.shared.application.exceptions import WishlistNotFound
from src.shared.ports.repository import BaseRepository


class WishlistRepository(BaseRepository[Wishlist]):
    @abc.abstractmethod
    def _list_all(self) -> list[Wishlist]: ...
    def list_all(self) -> list[Wishlist]:
        wishlists = self._list_all()
        self.seen.update(wishlists)
        return wishlists

    @abc.abstractmethod
    def _list_owned_by(self, username: str) -> list[Wishlist]: ...

    def list_owned_by(self, username: str) -> list[Wishlist]:
        wishlists = self._list_owned_by(username)
        self.seen.update(wishlists)
        return wishlists

    @abc.abstractmethod
    def _get(self, uuid: UUID) -> Wishlist: ...

    @abc.abstractmethod
    def _add(self, wishlist: Wishlist): ...


class FakeWishlistRepository(WishlistRepository):
    """In-memory implementation for unit tests."""

    def __init__(self, wishlists: set[Wishlist]):
        super().__init__()
        self._wishlists = wishlists

    def _get(self, uuid: UUID) -> Wishlist:
        try:
            wishlist = next(wl for wl in self._wishlists if wl.uuid == uuid)
        except StopIteration:
            raise WishlistNotFound(uuid=uuid)
        return wishlist

    def _list_all(self) -> list[Wishlist]:
        return list(self._wishlists)

    def _list_owned_by(self, username: str) -> list[Wishlist]:
        return list(wl for wl in self._wishlists if wl.owner_username == username)

    def _add(self, wishlist: Wishlist):
        self._wishlists.add(wishlist)
