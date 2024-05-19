import abc

from src.shared_kernel.service_layer.unit_of_work import AbstractUnitOfWork
from src.wishlist.infrastructure.wishlist_repository import WishlistRepository


class WishlistUnitOfWork(AbstractUnitOfWork):
    def __init__(self, wishlist_repository: WishlistRepository):
        self.wishlist_repository = wishlist_repository

    def collect_new_events(self):
        for wishlist in self.wishlist_repository.seen:
            while wishlist.events:
                yield wishlist.events.pop(0)

    @abc.abstractmethod
    def _commit(self): ...

    @abc.abstractmethod
    def _rollback(self): ...
