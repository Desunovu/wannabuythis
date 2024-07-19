from dataclasses import dataclass, field

from src.common.domain.aggregates import AggregateRoot
from src.common.service.exceptions import UserAlreadyActive, UserAlreadyDeactivated
from src.users.domain.events import (
    EmailChanged,
    PasswordChanged,
    UserActivated,
    UserCreated,
    UserDeactivated,
)


@dataclass(kw_only=True, unsafe_hash=True)
class User(AggregateRoot):
    username: str
    email: str
    password_hash: str
    is_active: bool = field(default=False)
    is_superuser: bool = field(default=False)

    def __post_init__(self):
        self._add_event(UserCreated(username=self.username, email=self.email))

    def change_password_hash(self, password_hash: str):
        """Setter for password hash"""
        self.password_hash = password_hash
        self._add_event(PasswordChanged(self.username))

    def change_email(self, email: str):
        self.email = email
        self._add_event(EmailChanged(self.username))

    def activate(self):
        if self.is_active:
            raise UserAlreadyActive(self.username)
        self.is_active = True
        self._add_event(UserActivated(self.username))

    def deactivate(self):
        if not self.is_active:
            raise UserAlreadyDeactivated(self.username)
        self.is_active = False
        self._add_event(UserDeactivated(self.username))
