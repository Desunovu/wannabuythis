import abc

from src.shared_kernel.service_layer.unit_of_work import AbstractUnitOfWork
from src.user.infrastructure.user_repository import UserRepository


class UserUnitOfWork(AbstractUnitOfWork):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def collect_new_events(self):
        for user in self.user_repository.seen:
            while user.events:
                yield user.events.pop(0)

    @abc.abstractmethod
    def _commit(self): ...

    @abc.abstractmethod
    def _rollback(self): ...
