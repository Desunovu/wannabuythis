from dataclasses import field


class Entity:
    id: int = field(init=False)


class AggregateRoot(Entity):
    pass
