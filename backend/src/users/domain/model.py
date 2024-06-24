from dataclasses import dataclass

from src.common.domain.aggregates import AggregateRoot
from src.common.domain.entities import Entity
from src.users.domain.events import (
    PasswordChanged,
    UserDeactivated,
    EmailChanged,
    RoleAddedToUser,
    RoleRemovedFromUser,
    UserActivated,
    UserCreated,
)


@dataclass
class Permission(Entity):
    name: str


class Role(Entity):
    def __init__(self, name: str):
        self.name = name
        self.permissions = []

    def has_permission(self, permission: Permission):
        return permission in self.permissions


class User(AggregateRoot):
    def __init__(self, username: str, email: str, password_hash: str):
        super().__init__()
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_active = False
        self.roles: list[Role] = []
        self.add_event(UserCreated(username=self.username, email=self.email))

    @staticmethod
    def validate_password(new_password: str) -> bool:
        """Rules for password validation"""
        if not new_password:
            return False
        if len(new_password) < 8:
            return False
        if not any(char.isdigit() for char in new_password):
            return False
        if not any(char.isupper() for char in new_password):
            return False
        return True

    def change_password_hash(self, password_hash: str):
        """Setter for password hash"""
        self.password_hash = password_hash
        self.add_event(PasswordChanged(self.username))

    def change_email(self, email: str):
        self.email = email
        self.add_event(EmailChanged(self.username))

    def activate(self):
        self.is_active = True
        self.add_event(UserActivated(self.username))

    def deactivate(self):
        self.is_active = False
        self.add_event(UserDeactivated(self.username))

    def add_role(self, role: Role):
        self.roles.append(role)
        self.add_event(RoleAddedToUser(self.username, role.name))

    def remove_role(self, role: Role):
        self.roles.remove(role)
        self.add_event(RoleRemovedFromUser(self.username, role.name))

    def has_role(self, role: Role) -> bool:
        return role in self.roles
