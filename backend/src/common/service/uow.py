import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.users.adapters.user_repository import UserRepository
    from src.wishlists.adapters.wishlist_repository import WishlistRepository


class AbstractUnitOfWork(abc.ABC):
    def __init__(
        self,
        user_repository: "UserRepository",
        wishlist_repository: "WishlistRepository",
    ):
        self.user_repository = user_repository
        self.wishlist_repository = wishlist_repository
        self.committed = None  # used only in tests

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self):
        for repository in (self.user_repository, self.wishlist_repository):
            for aggregate in repository.seen:
                while aggregate.events:
                    yield aggregate.events.pop(0)

    @abc.abstractmethod
    def _commit(self): ...

    @abc.abstractmethod
    def _rollback(self): ...
