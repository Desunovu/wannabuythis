import abc

from src.common.adapters.repository import BaseRepository
from src.users.domain.model import User


class UserRepository(BaseRepository[User]):
    @abc.abstractmethod
    def _get(self, username: str) -> User | None: ...

    @abc.abstractmethod
    def _add(self, user: User): ...
