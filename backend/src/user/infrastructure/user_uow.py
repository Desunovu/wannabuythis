import abc

from src.user.infrastructure.user_repository import UserRepository


class UserUnitOfWork(abc.ABC):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self):
        for user in self.user_repository.seen:
            while user.events:
                yield user.events.pop(0)

    @abc.abstractmethod
    def _commit(self): ...

    @abc.abstractmethod
    def rollback(self): ...
