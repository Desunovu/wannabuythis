from dataclasses import dataclass, field

from src.common.domain.aggregates import AggregateRoot
from src.common.domain.value_objects import ValueObject
from src.roles.domain.events import (
    PermissionAddedToRole,
    PermissionRemovedFromRole,
    RoleCreated,
)


@dataclass(frozen=True)
class Permission(ValueObject):
    name: str


@dataclass(kw_only=True, unsafe_hash=True)
class Role(AggregateRoot):
    name: str
    permissions: list = field(default_factory=list, compare=False)

    def __post_init__(self):
        self.add_event(RoleCreated(self.name))

    def has_permission(self, permission_name: str) -> bool:
        return permission_name in [p.name for p in self.permissions]

    def add_permission(self, permission: Permission):
        self.permissions.append(permission)
        self.add_event(
            PermissionAddedToRole(role_name=self.name, permission_name=permission.name)
        )

    def remove_permission(self, permission_name: str):
        self.permissions = [p for p in self.permissions if p.name != permission_name]
        self.add_event(
            PermissionRemovedFromRole(
                role_name=self.name, permission_name=permission_name
            )
        )
