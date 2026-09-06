from src.modules.users.infrastructure.user_repository import FakeUserRepository
from src.modules.wishlists.infrastructure.wishlist_repository import (
    FakeWishlistRepository,
)
from src.shared.application.uow import UnitOfWork


class FakeUnitOfWork(UnitOfWork):
    """In-memory unit of work for unit tests."""

    def __init__(self):
        super().__init__()
        self.user_repository = FakeUserRepository(users=set())
        self.wishlist_repository = FakeWishlistRepository(set())
        self.committed = False

    def _commit(self):
        self.committed = True

    def _rollback(self):
        pass