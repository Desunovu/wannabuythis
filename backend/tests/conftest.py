from uuid import uuid4

import pytest

from src.modules.users.domain.model import User
from src.modules.wishlists.domain.model import (
    MeasurementUnit,
    Priority,
    Wishlist,
    WishlistItem,
)
from src.shared.utils.auth.password_manager import Argon2PasswordManager


# General purpose fixtures
@pytest.fixture
def valid_password():
    return "StrongPassword123!"


@pytest.fixture
def valid_new_password():
    return "NEWStrongPassword123!"


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
        password_hash=Argon2PasswordManager().hash_password(valid_password),
        is_active=True,
    )


@pytest.fixture
def admin_user(admin_email, valid_password):
    return User(
        username="admin",
        email=admin_email,
        password_hash=Argon2PasswordManager().hash_password(valid_password),
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
