import abc

from src.common.adapters.repository import BaseRepository
from src.users.domain.model import User, Role


class UserRepository(BaseRepository[User]):
    @abc.abstractmethod
    def _get(self, username: str) -> User: ...

    @abc.abstractmethod
    def _add(self, user: User): ...

    @abc.abstractmethod
    def get_role_by_name(self, role_name: str) -> Role: ...
