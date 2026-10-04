import abc

from passlib.context import CryptContext
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

    @abc.abstractmethod
    def hash_password(self, password: str) -> str: ...

    @abc.abstractmethod
    def verify_password(self, password: str, password_hash: str) -> bool: ...

    def assert_passwords_match(self, password: str, password_hash: str):
        if not self.verify_password(password, password_hash):
            raise PasswordVerificationError


class Argon2PasswordManager(PasswordManager):
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["argon2"])

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, password_hash: str) -> bool:
        return self.pwd_context.verify(password, password_hash)
