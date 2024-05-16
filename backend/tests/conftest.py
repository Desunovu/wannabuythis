import pytest

from src.user.domain.user import User
from src.wishlist.domain.wishlist import Wishlist
from src.wishlist.domain.wishlist_item import MeasurementUnit, WishlistItem, Priority


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
        id=1,
        name="Banana",
        quantity=2,
        measurement_unit=measurement_unit,
        priority=priority,
    )


@pytest.fixture
def apple_item(measurement_unit, priority):
    """Just a banana wishlist item"""
    return WishlistItem(
        id=2,
        name="Apple",
        quantity=3,
        measurement_unit=measurement_unit,
        priority=priority,
    )


@pytest.fixture
def wishlist():
    """Empty wishlist"""
    return Wishlist(id=1, user_id=1, name="My new list")


@pytest.fixture
def populated_wishlist(banana_item, apple_item):
    """Wishlist with 2 different items"""
    populated_wishlist = Wishlist(id=2, user_id=1, name="My populated list")
    populated_wishlist.items = [banana_item, apple_item]
    return populated_wishlist


@pytest.fixture
def user():
    """User with no wishlists"""
    return User(id=1, name="testuser", email="testemail@example.com")


@pytest.fixture
def user_with_wishlists(user, wishlist, populated_wishlist):
    """User with 2 wishlists (one populated and one not)"""
    user.wishlists = [populated_wishlist, wishlist]
    return user
