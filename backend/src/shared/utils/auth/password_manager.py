import abc
import hashlib

from zxcvbn import zxcvbn

from src.shared.application.exceptions import (
    PasswordValidationError,
    PasswordVerificationError,
)


class PasswordManager(abc.ABC):
    @staticmethod
    def assert_password_valid(password: str, user_inputs: list | None = None):
        """Raises PasswordValidationError if the password does not meet the validation rules"""
        if len(password) < 8:
            raise PasswordValidationError("Password must be at least 8 characters long")

        results = zxcvbn(password, user_inputs=user_inputs)
        if results["score"] < 3:
            feedback = results["feedback"]["warning"] or "Password too weak"
            raise PasswordValidationError(feedback)

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
