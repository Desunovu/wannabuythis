import abc
from uuid import UUID, uuid4


class UUIDGenerator(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def generate() -> UUID: ...


class DefaultUUIDGenerator(UUIDGenerator):
    @staticmethod
    def generate() -> UUID:
        return uuid4()
