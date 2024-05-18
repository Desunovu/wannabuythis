from dataclasses import dataclass

from src.shared_kernel.events import DomainEvent


@dataclass
class UserCreated(DomainEvent):
    username: str


@dataclass
class PasswordChanged(DomainEvent):
    username: str
