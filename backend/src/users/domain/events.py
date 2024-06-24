from dataclasses import dataclass

from src.common.domain.events import DomainEvent


@dataclass
class UserCreated(DomainEvent):
    username: str
    email: str


@dataclass
class PasswordChanged(DomainEvent):
    username: str


@dataclass
class EmailChanged(DomainEvent):
    username: str


@dataclass
class UserActivated(DomainEvent):
    username: str


@dataclass
class UserDeactivated(DomainEvent):
    username: str


@dataclass
class RoleAddedToUser(DomainEvent):
    username: str
    role_name: str


@dataclass
class RoleRemovedFromUser(DomainEvent):
    username: str
    role_name: str
