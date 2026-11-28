import abc

from src.shared.domain.aggregates import AggregateRoot


class BaseRepository[T: AggregateRoot](abc.ABC):
    def __init__(self):
        self.seen: set[T] = set()

    @abc.abstractmethod
    def _get(self, identifier, /, *, for_update: bool = True) -> T | None: ...

    def get(self, identifier) -> T | None:
        """Load an aggregate for modification; implementations may lock its row."""
        return self._track(self._get(identifier, for_update=True))

    def get_readonly(self, identifier) -> T | None:
        """Load an aggregate without locking; for checks that do not modify it."""
        return self._track(self._get(identifier, for_update=False))

    def _track(self, item: T | None) -> T | None:
        if item:
            self.seen.add(item)
        return item

    @abc.abstractmethod
    def _add(self, item: T, /): ...

    def add(self, item: T):
        self._add(item)
        self.seen.add(item)
