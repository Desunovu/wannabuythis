import abc
from uuid import UUID

from src.common.adapters.repository import BaseRepository
from src.wishlists.domain.model import Wishlist


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
    def _add(self, user: Wishlist): ...
