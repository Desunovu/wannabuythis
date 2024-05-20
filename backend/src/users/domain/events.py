from dataclasses import dataclass

from src.common.domain.events import DomainEvent


@dataclass
class UserCreated(DomainEvent):
    username: str


@dataclass
class PasswordChanged(DomainEvent):
    username: str
