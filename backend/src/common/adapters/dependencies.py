import abc
import hashlib
from uuid import uuid4


class AbstractPasswordManager(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def hash_password(password: str) -> str: ...

    @staticmethod
    @abc.abstractmethod
    def verify_password(password: str, password_hash: str) -> bool: ...


class DefaultPasswordManager(AbstractPasswordManager):
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return DefaultPasswordManager.hash_password(password) == password_hash


class AbstractUUIDGenerator(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def generate() -> str: ...


class DefaultUUIDGenerator(AbstractUUIDGenerator):
    @staticmethod
    def generate() -> str:
        return str(uuid4())
