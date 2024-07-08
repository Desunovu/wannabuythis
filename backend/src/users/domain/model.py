from dataclasses import dataclass, field

from src.common.domain.aggregates import AggregateRoot
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
