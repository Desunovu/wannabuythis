from uuid import UUID, uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from src.bootstrap import bootstrap
from src.common.domain.entities import Role
from src.common.service.uow import UnitOfWork
from src.integration.adapters.sqlalchemy_orm import mapper_registry, start_mappers
from src.integration.service.sqlalchemy_uow import SQLAlchemyUnitOfWork
from src.roles.adapters.role_repository import RoleRepository
from src.users.adapters.user_repository import UserRepository
from src.users.domain.user import User
from src.wishlists.adapters.wishlist_repository import WishlistRepository
from src.wishlists.domain.wishlist import Wishlist
from src.wishlists.domain.wishlist_item import MeasurementUnit, WishlistItem, Priority


# Domain layer


@pytest.fixture
def user():
    """Default user"""
    return User(
        username="testuser", email="testemail@example.com", password_hash="password"
    )


@pytest.fixture
def admin_role() -> Role:
    return Role(name="admin")


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
def wishlist(user):
    """Empty wishlist"""
    return Wishlist(
        uuid=uuid4(), owner_username=user.username, name="My list", items=[]
    )


@pytest.fixture
def populated_wishlist(user, banana_item, apple_item):
    """Wishlist with 2 different items"""
    populated_wishlist = Wishlist(
        uuid=uuid4(),
        owner_username=user.username,
        name="My list",
        items=[banana_item, apple_item],
    )
    return populated_wishlist


# Service layer


class FakeUserRepository(UserRepository):
    def __init__(self, users: set[User]):
        super().__init__()
        self._users = users

    def _get(self, username: str) -> User | None:
        return next((user for user in self._users if user.username == username), None)

    def _add(self, user: User):
        self._users.add(user)


class FakeWishlistRepository(WishlistRepository):
    def __init__(self, wishlists: set[Wishlist]):
        super().__init__()
        self._wishlists = wishlists

    def _get(self, uuid: UUID) -> Wishlist | None:
        return next((wl for wl in self._wishlists if wl.uuid == uuid), None)

    def _list_all(self) -> list[Wishlist]:
        return list(self._wishlists)

    def _list_owned_by(self, username: str) -> list[Wishlist]:
        return list(wl for wl in self._wishlists if wl.owner_username == username)

    def _add(self, wishlist: Wishlist):
        self._wishlists.add(wishlist)


class FakeRoleRepository(RoleRepository):
    def __init__(self, roles: set[Role]):
        super().__init__()
        self._roles = roles

    def _get(self, name: str) -> Role | None:
        return next((role for role in self._roles if role.name == name), None)

    def _add(self, role: Role):
        self._roles.add(role)


class FakeUnitOfWork(UnitOfWork):
    def __init__(self):
        super().__init__()
        self.user_repository = FakeUserRepository(set())
        self.wishlist_repository = FakeWishlistRepository(set())
        self.role_repository = FakeRoleRepository(set())
        self.committed = False

    def _commit(self):
        self.committed = True

    def _rollback(self):
        pass


# TODO bootstrap messagebus
@pytest.fixture
def messagebus():
    return bootstrap(uow=FakeUnitOfWork())


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


# Integration Tests


@pytest.fixture
def mappers():
    start_mappers()
    yield
    clear_mappers()


@pytest.fixture
def sqlite_database_engine(mappers):
    # Create an in-memory SQLite database
    engine = create_engine("sqlite:///:memory:")
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
