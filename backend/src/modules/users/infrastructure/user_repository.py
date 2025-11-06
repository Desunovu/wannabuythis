import abc

from src.modules.users.domain.model import User
from src.shared.application.exceptions import (
    UserActive,
    UserExists,
    UserNotActive,
    UserNotFound,
)
from src.shared.ports.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    @abc.abstractmethod
    def _get(self, username: str) -> User: ...

    @abc.abstractmethod
    def _add(self, user: User): ...

    def assert_user_does_not_exist(self, username: str):
        try:
            self._get(username)
        except UserNotFound:
            return
        raise UserExists(username=username)

    def get_active_user(self, username: str) -> User:
        user = self._get(username)
        if not user.is_active:
            raise UserNotActive(username)
        return user

    def get_inactive_user(self, username: str) -> User:
        user = self._get(username)
        if user.is_active:
            raise UserActive(username)
        return user
