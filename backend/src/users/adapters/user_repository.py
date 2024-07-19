import abc

from src.common.adapters.repository import BaseRepository
from src.common.service.exceptions import UserExists, UserNotFound
from src.users.domain.model import User


class UserRepository(BaseRepository[User]):
    def assert_user_does_not_exist(self, username: str):
        try:
            self._get(username)
        except UserNotFound:
            return
        raise UserExists(username=username)

    @abc.abstractmethod
    def _get(self, username: str) -> User: ...

    @abc.abstractmethod
    def _add(self, user: User): ...
