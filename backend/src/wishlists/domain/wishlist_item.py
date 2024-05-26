from dataclasses import dataclass
from uuid import UUID

from src.common.domain.entities import Entity
from src.common.domain.value_objects import ValueObject


@dataclass
class MeasurementUnit(ValueObject):
    name: str


@dataclass
class Priority(ValueObject):
    value: int


class WishlistItem(Entity):
    def __init__(
        self,
        uuid: UUID,
        wishlist_uuid: UUID,
        name: str,
        quantity: int,
        measurement_unit: MeasurementUnit,
        priority: Priority,
    ):
        super().__init__()
        self.uuid = uuid
        self.wishlist_uuid = wishlist_uuid
        self.name = name
        self.quantity = quantity
        self.measurement_unit = measurement_unit
        self.priority = priority
        self.is_purchased = False
