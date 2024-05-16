import abc

from src.user.domain.user import User


class UserRepository(abc.ABC):
    def __init__(self):
        self.seen: set[User] = set()

    def get(self, user_id: int) -> User:
        user = self._get(user_id)
        if user:
            self.seen.add(user)
        return user

    def add(self, user: User):
        self._add(user)
        self.seen.add(user)

    @abc.abstractmethod
    def _get(self, user_id: int) -> User: ...

    @abc.abstractmethod
    def _add(self, user: User): ...
