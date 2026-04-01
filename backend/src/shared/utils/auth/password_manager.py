import abc
import logging

from passlib.context import CryptContext
from zxcvbn import zxcvbn

from src.shared.application.exceptions import (
    PasswordValidationError,
    PasswordVerificationError,
)

logger = logging.getLogger(__name__)


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
    def verify_password(cls, password: str, password_hash: str) -> bool: ...

    def assert_passwords_match(self, password: str, password_hash: str):
        if not self.verify_password(password, password_hash):
            raise PasswordVerificationError


class Argon2PasswordManager(PasswordManager):
    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=["argon2", "hex_sha256"], default="argon2", deprecated="auto"
        )

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, password_hash: str) -> bool:
        is_valid, new_hash = self.pwd_context.verify_and_update(password, password_hash)
        if new_hash:
            logger.warning(
                f"Password hash needs to be updated (old_hash={password_hash}, new_hash={new_hash})"
            )
        return is_valid
