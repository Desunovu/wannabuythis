from dataclasses import dataclass

from src.shared_kernel.entities import Entity
from src.shared_kernel.value_objects import ValueObject


@dataclass
class MeasurementUnit(ValueObject):
    name: str


@dataclass
class Priority(ValueObject):
    value: int


class WishlistItem(Entity):
    def __init__(
        self,
        id: int,
        name: str,
        quantity: int,
        measurement_unit: MeasurementUnit,
        priority: Priority,
    ):
        super().__init__(id)
        self.name = name
        self.quantity = quantity
        self.measurement_unit = measurement_unit
        self.priority = priority
