import abc


class AbstractUnitOfWork(abc.ABC):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._rollback()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def _commit(self): ...

    @abc.abstractmethod
    def _rollback(self): ...

    @abc.abstractmethod
    def collect_new_events(self): ...
