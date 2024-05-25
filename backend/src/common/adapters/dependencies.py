import abc
import hashlib
from uuid import uuid4, UUID


class PasswordHasher(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def hash_password(password: str) -> str: ...

    @staticmethod
    @abc.abstractmethod
    def verify_password(password: str, password_hash: str) -> bool: ...


class DefaultPasswordHasher(PasswordHasher):
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return DefaultPasswordHasher.hash_password(password) == password_hash


class UUIDGenerator(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def generate() -> UUID: ...


class DefaultUUIDGenerator(UUIDGenerator):
    @staticmethod
    def generate() -> UUID:
        return uuid4()
