import pytest

from src.adapters.user_repository import UserRepository
from src.adapters.wishlist_repository import WishlistRepository
from src.domain.user.commands import CreateUser, ChangePassword
from src.domain.user.user import User
from src.domain.wishlist.wishlist import Wishlist
from src.service_layer.messagebus import Messagebus
from src.service_layer.unit_of_work import AbstractUnitOfWork
from src.service_layer.user_handlers import (
    COMMAND_HANDLERS,
    EVENT_HANDLERS,
    UserNotFound,
    UserExists,
)


class FakeUserRepository(UserRepository):
    def __init__(self, users: set[User]):
        super().__init__()
        self._users = set(users)

    def _get(self, username: str) -> User | None:
        return next((user for user in self._users if user.username == username), None)

    def _add(self, user: User):
        self._users.add(user)


class FakeWishlistRepository(WishlistRepository):
    def __init__(self, wishlists: set[Wishlist]):
        super().__init__()
        self._wishlists = set(wishlists)

    def _get(self, uuid: str) -> Wishlist | None:
        return next((wl for wl in self._wishlists if wl.uuid == uuid), None)

    def _add(self, wishlist: Wishlist):
        self._wishlists.add(wishlist)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        super().__init__(FakeUserRepository(set()), FakeWishlistRepository(set()))
        self.committed = False

    def _commit(self):
        self.committed = True

    def _rollback(self):
        pass


# TODO bootstrap messagebus
@pytest.fixture
def messagebus():
    return Messagebus(
        uow=FakeUnitOfWork(),
        command_handlers=COMMAND_HANDLERS,
        event_handlers=EVENT_HANDLERS,
    )


class TestCreateUser:
    def test_create_new_user(self, messagebus):
        messagebus.handle(CreateUser("testuser", "testemail@example.com", "password"))

        assert messagebus.uow.user_repository.get("testuser") is not None

    def test_create_existing_user(self, messagebus):
        messagebus.handle(CreateUser("testuser", "testemail@example.com", "password"))

        with pytest.raises(UserExists):
            messagebus.handle(
                CreateUser("testuser", "testemail@example.com", "password")
            )


class TestChangePassword:
    def test_change_password(self, messagebus):
        messagebus.handle(CreateUser("testuser", "testemail@example.com", "password"))
        user = messagebus.uow.user_repository.get("testuser")
        old_password_hash = user.password_hash
        messagebus.handle(ChangePassword("testuser", "newpassword"))

        assert user.password_hash != old_password_hash

    def test_change_password_non_existing_user(self, messagebus):
        with pytest.raises(UserNotFound):
            messagebus.handle(ChangePassword("testuser", "newpassword"))

    # TODO add test for wrong password
