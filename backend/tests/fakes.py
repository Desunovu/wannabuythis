from uuid import UUID

from src.common.dependencies.notificator import Notificator
from src.common.service.exceptions import UserNotFound, WishlistNotFound
from src.common.service.uow import UnitOfWork
from src.users.adapters.user_repository import UserRepository
from src.users.domain.model import User
from src.wishlists.adapters.wishlist_repository import WishlistRepository
from src.wishlists.domain.model import Wishlist


class FakeUserRepository(UserRepository):
    def __init__(self, users: set[User]):
        super().__init__()
        self._users = users

    def _get(self, username: str) -> User:
        try:
            user = next(user for user in self._users if user.username == username)
        except StopIteration:
            raise UserNotFound(username=username)
        return user

    def _add(self, user: User):
        self._users.add(user)


class FakeWishlistRepository(WishlistRepository):
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


class FakeUnitOfWork(UnitOfWork):
    def __init__(self):
        super().__init__()
        self.user_repository = FakeUserRepository(users=set())
        self.wishlist_repository = FakeWishlistRepository(set())
        self.committed = False

    def _commit(self):
        self.committed = True

    def _rollback(self):
        pass


class FakeNotificator(Notificator):
    def send_notification(self, recipient: "User", subject: str, message: str) -> None:
        print(
            f"Fake notificator: {recipient.username} ({recipient.email}), {subject}, {message}"
        )
