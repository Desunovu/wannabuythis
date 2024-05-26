from dataclasses import dataclass


class Entity:
    pass


@dataclass
class Permission(Entity):
    name: str


class Role(Entity):
    def __init__(self, name: str):
        self.name = name
        self.permissions = []

    def has_permission(self, permission: Permission):
        return permission in self.permissions
