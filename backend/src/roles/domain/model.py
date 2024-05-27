from dataclasses import dataclass

from src.common.domain.aggregates import AggregateRoot
from src.common.domain.value_objects import ValueObject


@dataclass
class Permission(ValueObject):
    name: str


class Role(AggregateRoot):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.permissions = []
