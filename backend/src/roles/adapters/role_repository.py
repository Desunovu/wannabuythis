import abc

from src.roles.domain.model import Role


class RoleRepository(abc.ABC):
    def __init__(self):
        self.seen: set[Role] = set()

    def get(self, name) -> Role | None:
        role = self._get(name)
        if role:
            self.seen.add(role)
        return role

    def add(self, role: Role):
        self._add(role)
        self.seen.add(role)

    @abc.abstractmethod
    def _get(self, name) -> Role | None: ...

    @abc.abstractmethod
    def _add(self, role: Role): ...
