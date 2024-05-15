import pytest
from faker import Faker

from src.shopping_list.domain.model import ShoppingItem, MeasurementUnit

fake = Faker()


@pytest.fixture
def random_shopping_item():

    def make(item_id=0):

        # Генерируем случайные данные для элемента списка покупок
        name = fake.word()
        category = fake.word()
        price = fake.pyfloat(positive=True)
        quantity = fake.random_int(min=1, max=10)
        unit_name = fake.word()

        # Создаем экземпляр объекта ShoppingItem с уникальным идентификатором
        shopping_item = ShoppingItem(
            name=name,
            category=category,
            price=price,
            quantity=quantity,
            unit=MeasurementUnit(name=unit_name),
        )
        shopping_item.id = item_id

        return shopping_item

    return make
