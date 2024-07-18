from uuid import uuid4

import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from src import bootstrap
from src.common.utils.activation_code_generator import (
    RandomActivationCodeGenerator,
)
from src.common.utils.password_hash_util import HashlibPasswordHashUtil
from src.common.utils.token_manager import JWTManager
from src.common.utils.uuid_generator import DefaultUUIDGenerator
from src.integration.adapters.sqlalchemy_orm import (
    mapper_registry,
    start_sqlalchemy_mappers,
)
from src.integration.service.sqlalchemy_uow import SQLAlchemyUnitOfWork
from src.users.domain.model import User
from src.wishlists.domain.model import MeasurementUnit, Priority, Wishlist, WishlistItem
from tests.fakes import FakeActivationCodeStorage, FakeNotificator, FakeUnitOfWork


# General purpose fixtures
@pytest.fixture
def valid_password():
    return "passWORD123"


@pytest.fixture
def valid_new_password():
    return "NEWpassWORD123"


@pytest.fixture
def invalid_password():
    return "123"


@pytest.fixture
def email():
    return "testemail@example.com"


@pytest.fixture
def new_email():
    return "newtestemail@example.com"


@pytest.fixture
def admin_email():
    return "admin@example.com"


@pytest.fixture
def wishlist_name():
    return "My wishlist"


@pytest.fixture
def wishlist_new_name():
    return "My new wishlist name"


# User fixtures
@pytest.fixture
def user(email, valid_password):
    return User(
        username="testuser",
        email=email,
        password_hash=HashlibPasswordHashUtil.hash_password(valid_password),
        is_active=True,
    )


@pytest.fixture
def admin_user(admin_email, valid_password):
    return User(
        username="admin",
        email=admin_email,
        password_hash=HashlibPasswordHashUtil.hash_password(valid_password),
        is_active=True,
        is_superuser=True,
    )


@pytest.fixture
def deactivated_user(user):
    user.is_active = False
    return user


@pytest.fixture
def activated_user(user):
    user.is_active = True
    return user


# Wishlist fixtures
@pytest.fixture
def measurement_unit():
    return MeasurementUnit.KILOGRAM


@pytest.fixture
def priority():
    return Priority(value=1)


@pytest.fixture
def purchased_banana_item(measurement_unit, priority):
    return WishlistItem(
        uuid=uuid4(),
        wishlist_uuid=uuid4(),
        name="Banana",
        quantity=2,
        measurement_unit=measurement_unit,
        priority=priority,
        is_purchased=True,
    )


@pytest.fixture
def apple_item(measurement_unit, priority):
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
    return Wishlist(
        uuid=uuid4(), owner_username=user.username, name=wishlist_name, items=[]
    )


@pytest.fixture
def populated_wishlist(user, purchased_banana_item, apple_item, wishlist_name):
    """Wishlist with banana (purchased) and apple items"""
    populated_wishlist = Wishlist(
        uuid=uuid4(),
        owner_username=user.username,
        name=wishlist_name,
        items=[purchased_banana_item, apple_item],
    )
    purchased_banana_item.wishlist_uuid = populated_wishlist.uuid
    apple_item.wishlist_uuid = populated_wishlist.uuid
    return populated_wishlist


@pytest.fixture
def archived_wishlist(wishlist):
    wishlist.is_archived = True
    return wishlist


# ORM, Database and session fixtures
@pytest.fixture
def prepare_mappers():
    start_sqlalchemy_mappers()
    yield
    clear_mappers()


@pytest.fixture
def sqlite_database_engine(prepare_mappers):
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


# Messagebus fixture
@pytest.fixture
def messagebus():
    dependencies = bootstrap.create_dependencies_dict(
        uow=FakeUnitOfWork(),
        password_hash_util=HashlibPasswordHashUtil(),
        uuid_generator=DefaultUUIDGenerator(),
        activation_code_generator=RandomActivationCodeGenerator(),
        activation_code_storage=FakeActivationCodeStorage(),
        token_manager=JWTManager(),
        notificator=FakeNotificator(),
    )
    return bootstrap.initialize_messagebus(dependencies=dependencies)
