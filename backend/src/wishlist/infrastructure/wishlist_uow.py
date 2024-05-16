import abc

from src.wishlist.infrastructure.wishlist_repository import WishlistRepository


class WishlistUnitOfWork:
    def __init__(self, wishlist_repository: WishlistRepository):
        self.wishlist_repository = wishlist_repository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self):
        for wishlist in self.wishlist_repository.seen:
            while wishlist.events:
                yield wishlist.events.pop(0)

    @abc.abstractmethod
    def _commit(self): ...

    @abc.abstractmethod
    def rollback(self): ...
