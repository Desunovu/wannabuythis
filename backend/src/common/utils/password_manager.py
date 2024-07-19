import abc
import hashlib

from src.common.service.exceptions import (
    PasswordValidationError,
    PasswordVerificationError,
)


class PasswordManager(abc.ABC):
    @staticmethod
    def assert_password_valid(new_password: str):
        """Raises PasswordValidationError if the password does not meet the validation rules"""
        password_length = len(new_password)
        has_digit = any(char.isdigit() for char in new_password)
        has_uppercase = any(char.isupper() for char in new_password)

        if not (password_length >= 8 and has_digit and has_uppercase):
            raise PasswordValidationError

    @classmethod
    @abc.abstractmethod
    def _verify_password_with_hash(cls, password: str, password_hash: str) -> bool: ...

    @classmethod
    def assert_passwords_match(cls, password: str, password_hash: str):
        if not cls._verify_password_with_hash(password, password_hash):
            raise PasswordVerificationError

    @staticmethod
    @abc.abstractmethod
    def hash_password(password: str) -> str: ...


class HashlibPasswordManager(PasswordManager):
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    def _verify_password_with_hash(cls, password: str, password_hash: str) -> bool:
        return password_hash == cls.hash_password(password)
