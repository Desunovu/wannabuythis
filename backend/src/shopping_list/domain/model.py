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
    name: str
    items: list[ShoppingItem]

    def add_item(self, item: ShoppingItem):
        pass

    def remove_item(self, item_id: int):
        pass
