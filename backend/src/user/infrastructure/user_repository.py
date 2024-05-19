import abc

from src.user.domain.user import User


class UserRepository(abc.ABC):
    def __init__(self):
        self.seen: set[User] = set()

    def get(self, username: str) -> User | None:
        user = self._get(username)
        if user:
            self.seen.add(user)
        return user

    def add(self, user: User):
        self._add(user)
        self.seen.add(user)

    @abc.abstractmethod
    def _get(self, username: str) -> User | None: ...

    @abc.abstractmethod
    def _add(self, user: User): ...
