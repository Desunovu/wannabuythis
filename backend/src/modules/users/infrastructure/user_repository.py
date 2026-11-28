import abc

from src.modules.users.domain.model import User
from src.shared.application.exceptions import (
    UserActive,
    UserEmailExists,
    UserExists,
    UserNotActive,
    UserNotFound,
)
from src.shared.domain.username import normalize_username
from src.shared.ports.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def _get(self, username: str, *, for_update: bool = True) -> User:
        return self._get_by_username(
            normalize_username(username), for_update=for_update
        )

    @abc.abstractmethod
    def _get_by_username(self, username: str, *, for_update: bool = True) -> User: ...

    @abc.abstractmethod
    def _get_by_email(self, email: str) -> User: ...

    @abc.abstractmethod
    def _add(self, user: User): ...

    def assert_user_does_not_exist(self, username: str):
        try:
            self.get_readonly(username)
        except UserNotFound:
            return
        raise UserExists(username=username)

    def assert_email_does_not_exist(self, email: str):
        try:
            self._get_by_email(email)
        except UserNotFound:
            return
        raise UserEmailExists(email=email)

    def get_active_user(self, username: str) -> User:
        user = self._get(username, for_update=True)
        if not user.is_active:
            raise UserNotActive(username)
        return user

    def get_inactive_user(self, username: str) -> User:
        """Load an inactive user without locking; use get() for modifications."""
        user = self._get(username, for_update=False)
        if user.is_active:
            raise UserActive(username)
        return user


class FakeUserRepository(UserRepository):
    """In-memory implementation for unit tests."""

    def __init__(self, users: set[User]):
        super().__init__()
        self._users = users

    def _get_by_username(self, username: str, *, for_update: bool = True) -> User:
        try:
            user = next(user for user in self._users if user.username == username)
        except StopIteration:
            raise UserNotFound(username=username)
        return user

    def _get_by_email(self, email: str) -> User:
        try:
            user = next(user for user in self._users if user.email == email)
        except StopIteration:
            raise UserNotFound(username=email)
        return user

    def _add(self, user: User):
        self._users.add(user)
