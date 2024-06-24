import abc

from src.common.adapters.repository import BaseRepository
from src.roles.domain.model import Role


class RoleRepository(BaseRepository[Role]):
    @abc.abstractmethod
    def _get(self, name) -> Role: ...

    @abc.abstractmethod
    def _add(self, role: Role): ...
