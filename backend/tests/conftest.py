from uuid import UUID, uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from src.bootstrap import bootstrap
from src.common.adapters.dependencies import (
    DefaultPasswordHasher,
    FakeNotificator,
    JWTManager,
)
from src.common.service.uow import UnitOfWork
from src.integration.adapters.sqlalchemy_orm import mapper_registry, start_mappers
from src.integration.service.sqlalchemy_uow import SQLAlchemyUnitOfWork
from src.roles.adapters.role_repository import RoleRepository
from src.roles.domain import model as role_domain_model
from src.users.adapters.user_repository import UserRepository
from src.users.domain.model import User, Role, Permission
from src.users.service.user_auth_service import UserAuthService
from src.wishlists.adapters.wishlist_repository import WishlistRepository
from src.wishlists.domain.model import Wishlist, MeasurementUnit, Priority, WishlistItem


@pytest.fixture
def user(user_email, valid_password):
    """Default user with #valid_password"""
    user = User(
        username="testuser",
        email=user_email,
        password_hash=DefaultPasswordHasher.hash_password(valid_password),
    )
    user.is_active = True
    return user


@pytest.fixture
def admin_user(user, admin_role):
    user.roles.append(admin_role)
    return user


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
def admin_role() -> Role:
    """Role entity from users bounded context"""
    return Role(name="admin")


@pytest.fixture
def permission():
    return Permission(name="CREATE_WISHLIST")


@pytest.fixture
def default_role():
    """Role aggregate from roles bounded context"""
    return role_domain_model.Role(name="default")


@pytest.fixture
def role_with_permissions(default_role, permission):
    """Role aggregate with permissions"""
    default_role.permissions.append(permission)
    return default_role


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


# TODO inject dependencies in UserAuthService
@pytest.fixture
def user_auth_service(messagebus):
    return UserAuthService(
        password_manager=DefaultPasswordHasher(),
        token_manager=JWTManager(),
        uow=messagebus.uow,
    )


@pytest.fixture
def messagebus():
    return bootstrap(uow=FakeUnitOfWork(), notificator=FakeNotificator())


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
def wishlist_name():
    """Default wishlist name. Used in wishlist fixture"""
    return "My wishlist"


@pytest.fixture
def wishlist_new_name():
    """Wishlist name used for wishlist name change test"""
    return "My new wishlist name"


@pytest.fixture
def prepare_mappers():
    start_mappers()
    yield
    clear_mappers()


@pytest.fixture
def sqlite_database_engine(prepare_mappers):
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
