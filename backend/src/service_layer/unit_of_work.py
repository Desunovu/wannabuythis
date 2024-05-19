import abc

from src.user.infrastructure.user_repository import UserRepository
from src.wishlist.infrastructure.wishlist_repository import WishlistRepository


class AbstractUnitOfWork(abc.ABC):
    def __init__(self, user_repository: UserRepository, wishlist_repository: WishlistRepository):
        self.user_repository = user_repository
        self.wishlist_repository = wishlist_repository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self): ...

    @abc.abstractmethod
    def _commit(self): ...

    @abc.abstractmethod
    def _rollback(self): ...
