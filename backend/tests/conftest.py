from uuid import UUID, uuid4

import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, clear_mappers

from src import bootstrap
from src.common.dependencies.notificator import Notificator
from src.common.dependencies.password_hash_util import HashlibPasswordHashUtil
from src.common.dependencies.token_manager import JWTManager
from src.common.dependencies.uuid_generator import DefaultUUIDGenerator
from src.common.service.exceptions import WishlistNotFound, UserNotFound
from src.common.service.uow import UnitOfWork
from src.integration.adapters.sqlalchemy_orm import (
    mapper_registry,
    start_sqlalchemy_mappers,
)
from src.integration.service.sqlalchemy_uow import SQLAlchemyUnitOfWork
from src.users.adapters.user_repository import UserRepository
from src.users.domain.model import User
from src.wishlists.adapters.wishlist_repository import WishlistRepository
from src.wishlists.domain.model import Wishlist, MeasurementUnit, Priority, WishlistItem


@pytest.fixture
def user(user_email, valid_password):
    """Default active user with #valid_password"""
    user = User(
        username="testuser",
        email=user_email,
        password_hash=HashlibPasswordHashUtil.hash_password(valid_password),
        is_active=True,
    )
    return user


@pytest.fixture
def admin_user(admin_email, valid_password):
    """Admin user"""
    admin = User(
        username="admin",
        email=admin_email,
        password_hash=HashlibPasswordHashUtil.hash_password(valid_password),
        is_active=True,
        is_superuser=True,
    )
    return admin


@pytest.fixture
def deactivated_user(user):
    """User with is_active=False"""
    user.is_active = False
    return user


@pytest.fixture
def activated_user(user):
    """User with is_active=True"""
    user.is_active = True
    return user


@pytest.fixture
def measurement_unit():
    return MeasurementUnit.KILOGRAM


@pytest.fixture
def priority():
    return Priority(value=1)


@pytest.fixture
def banana_item(measurement_unit, priority):
    """Just a banana wishlist item"""
    return WishlistItem(
        uuid=uuid4(),
        wishlist_uuid=uuid4(),
        name="Banana",
        quantity=2,
        measurement_unit=measurement_unit,
        priority=priority,
    )


@pytest.fixture
def apple_item(measurement_unit, priority):
    """Just an apple wishlist item"""
    return WishlistItem(
        uuid=uuid4(),
        wishlist_uuid=uuid4(),
        name="Apple",
        quantity=3,
        measurement_unit=measurement_unit,
        priority=priority,
    )


@pytest.fixture
def wishlist(user, wishlist_name):
    """Empty wishlist"""
    return Wishlist(
        uuid=uuid4(), owner_username=user.username, name=wishlist_name, items=[]
    )


@pytest.fixture
def populated_wishlist(user, banana_item, apple_item, wishlist_name):
    """Wishlist containing two wishlist items"""
    populated_wishlist = Wishlist(
        uuid=uuid4(),
        owner_username=user.username,
        name=wishlist_name,
        items=[],
    )
    banana_item.wishlist_uuid = populated_wishlist.uuid
    apple_item.wishlist_uuid = populated_wishlist.uuid
    populated_wishlist.items = [banana_item, apple_item]
    return populated_wishlist


@pytest.fixture
def archived_wishlist(wishlist):
    """Archived wishlist"""
    wishlist.is_archived = True
    return wishlist


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


@pytest.fixture
def messagebus():
    dependencies = bootstrap.initialize_dependencies(
        uow=FakeUnitOfWork(),
        password_hash_util=HashlibPasswordHashUtil(),
        uuid_generator=DefaultUUIDGenerator(),
        token_manager=JWTManager(),
        notificator=FakeNotificator(),
    )
    return bootstrap.initialize_messagebus(dependencies=dependencies)


@pytest.fixture
def valid_password():
    """Valid password. Used in user fixture"""
    return "passWORD123"


@pytest.fixture
def valid_new_password():
    """Another valid password used for password change test"""
    return "NEWpassWORD123"


@pytest.fixture
def invalid_password():
    return "123"


@pytest.fixture
def user_email():
    """Default user email. Used in user fixture"""
    return "testemail@example.com"


@pytest.fixture
def new_email():
    """User email used for email change test"""
    return "newtestemail@example.com"


@pytest.fixture
def admin_email():
    """Admin user email. Used in admin_user fixture"""
    return "admin@example.com"


@pytest.fixture
def wishlist_name():
    """Default wishlist name. Used in wishlist fixture"""
    return "My wishlist"


@pytest.fixture
def wishlist_new_name():
    """Wishlist name used for wishlist name change test"""
    return "My new wishlist name"


@pytest.fixture
def prepare_mappers():
    start_sqlalchemy_mappers()
    yield
    clear_mappers()


@pytest.fixture
def sqlite_database_engine(prepare_mappers):
    # Create an in-memory SQLite database
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    mapper_registry.metadata.create_all(engine)
    yield engine
    mapper_registry.metadata.drop_all(engine)


@pytest.fixture
def sqlite_session_factory(sqlite_database_engine):
    yield sessionmaker(bind=sqlite_database_engine)


@pytest.fixture
def sqlite_session(sqlite_session_factory):
    session = sqlite_session_factory()
    yield session
    session.close()


@pytest.fixture
def sqlalchemy_uow(sqlite_session_factory):
    return SQLAlchemyUnitOfWork(sqlite_session_factory)
