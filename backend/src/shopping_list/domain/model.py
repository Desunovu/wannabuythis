from dataclasses import dataclass

from src.shared_kernel.domain.entity import AggregateRoot, Entity
from src.shared_kernel.domain.value_object import ValueObject


@dataclass
class MeasurementUnit(ValueObject):
    name: str


@dataclass
class ShoppingItem(Entity):
    name: str
    category: str
    price: float
    quantity: int
    unit: MeasurementUnit


class ShoppingList(AggregateRoot):
    def __init__(self, name: str, items: list[ShoppingItem]):
        self.name = name
        self._items = items

    @property
    def items(self):
        return self._items

    def add_item(self, item: ShoppingItem):
        self._items.append(item)

    def remove_item(self, item_id: int):
        item = next(i for i in self._items if i.id == item_id)
        self._items.remove(item)
