import pytest

from src.shopping_list.domain.model import ShoppingItem, MeasurementUnit, ShoppingList
from src.user.domain.model import User


@pytest.fixture
def measurement_unit():
    return MeasurementUnit(name="kg.")


@pytest.fixture
def banana_item(measurement_unit):
    banana_item = ShoppingItem(
        name="Banana",
        category="Food",
        price=1.0,
        quantity=2,
        unit=measurement_unit,
    )
    banana_item.id = 1
    return banana_item


@pytest.fixture
def apple_item(measurement_unit):
    apple_item = ShoppingItem(
        name="Apple",
        category="Food",
        price=1.0,
        quantity=3,
        unit=measurement_unit,
    )
    apple_item.id = 2
    return apple_item


@pytest.fixture
def shopping_list():
    shopping_list = ShoppingList(name="My shopping list", items=[])
    shopping_list.id = 1
    return shopping_list


@pytest.fixture
def populated_shopping_list(banana_item, apple_item):
    shopping_list = ShoppingList(
        name="My populated shopping list", items=[banana_item, apple_item]
    )
    shopping_list.id = 2
    return shopping_list


@pytest.fixture
def user():
    user = User(
        username="testuser",
        email="testemail@example.com",
        password_hash="testpassword",
        shopping_lists=[],
    )
    user.id = 1
    return user


@pytest.fixture
def user_with_shopping_lists(shopping_list, populated_shopping_list):
    user = User(
        username="testuser2",
        email="testemail2@example.com",
        password_hash="testpassword2",
        shopping_lists=[shopping_list, populated_shopping_list],
    )
    user.id = 2
    return user
