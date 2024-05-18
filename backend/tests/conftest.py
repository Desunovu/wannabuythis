import pytest

from src.user.domain.user import User
from src.wishlist.domain.wishlist import Wishlist
from src.wishlist.domain.wishlist_item import MeasurementUnit, WishlistItem, Priority


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
