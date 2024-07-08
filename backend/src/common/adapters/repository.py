import abc
from typing import Generic, Optional, TypeVar

from src.common.domain.aggregates import AggregateRoot

T = TypeVar("T", bound=AggregateRoot)


class BaseRepository(abc.ABC, Generic[T]):
    def __init__(self):
        self.seen: set[T] = set()

    @abc.abstractmethod
    def _get(self, identifier) -> Optional[T]: ...

    def get(self, identifier) -> Optional[T]:
        item = self._get(identifier)
        if item:
            self.seen.add(item)
        return item

    @abc.abstractmethod
    def _add(self, item: T): ...

    def add(self, item: T):
        self._add(item)
        self.seen.add(item)
