import pytest

from src.adapters.user_repository import UserRepository
from src.adapters.wishlist_repository import WishlistRepository
from src.domain.user.user import User
from src.domain.wishlist.wishlist import Wishlist
from src.domain.wishlist.wishlist_item import MeasurementUnit, WishlistItem, Priority
from src.service_layer.messagebus import Messagebus
from src.service_layer.unit_of_work import AbstractUnitOfWork
from src.service_layer.user_handlers import COMMAND_HANDLERS, EVENT_HANDLERS


# Domain layer


@pytest.fixture
def user():
    """Default user"""
    return User(
        username="testuser", email="testemail@example.com", password_hash="password"
    )


@pytest.fixture
def measurement_unit():
    return MeasurementUnit(name="kg.")


@pytest.fixture
def priority():
    return Priority(value=1)


@pytest.fixture
def banana_item(measurement_unit, priority):
    """Just a banana wishlist item"""
    return WishlistItem(
        uuid="banana-uuid",
        name="Banana",
        quantity=2,
        measurement_unit=measurement_unit,
        priority=priority,
    )


@pytest.fixture
def apple_item(measurement_unit, priority):
    """Just an apple wishlist item"""
    return WishlistItem(
        uuid="apple-uuid",
        name="Apple",
        quantity=3,
        measurement_unit=measurement_unit,
        priority=priority,
    )


@pytest.fixture
def wishlist(user):
    """Empty wishlist"""
    return Wishlist(
        uuid="wishlist-uuid", owner_username=user.username, name="My list", items=[]
    )


@pytest.fixture
def populated_wishlist(user, banana_item, apple_item):
    """Wishlist with 2 different items"""
    populated_wishlist = Wishlist(
        uuid="populated-wishlist-uuid",
        owner_username=user.username,
        name="My list",
        items=[banana_item, apple_item],
    )
    return populated_wishlist


# Service layer


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


@pytest.fixture
def valid_password():
    return "passWORD123"


@pytest.fixture
def valid_old_password():
    return "OLDpassWORD123"


@pytest.fixture
def invalid_password():
    return "123"


@pytest.fixture
def invalid_old_password():
    return "123"
