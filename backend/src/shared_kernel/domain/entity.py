from dataclasses import field, dataclass


class Entity:
    id: int = field(init=False)


class AggregateRoot(Entity):
    def __init__(self):
        self.events = []
