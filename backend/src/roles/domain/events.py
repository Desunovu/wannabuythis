from dataclasses import dataclass

from src.common.domain.events import DomainEvent


@dataclass
class RoleCreated(DomainEvent):
    role_name: str


@dataclass
class PermissionAddedToRole(DomainEvent):
    role_name: str
    permission_name: str


@dataclass
class PermissionRemovedFromRole(DomainEvent):
    role_name: str
    permission_name: str
