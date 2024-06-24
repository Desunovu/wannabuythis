import abc
import datetime
import hashlib
from uuid import uuid4, UUID

import jwt

from src import config


class AuthTokenManager(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def generate_token(email: str) -> str: ...

    @staticmethod
    @abc.abstractmethod
    def get_email_from_token(token: str) -> str: ...


class JWTManager(AuthTokenManager):
    @staticmethod
    def generate_token(email: str) -> str:
        token = jwt.encode(
            {
                "email": email,
                "exp": datetime.datetime.now(datetime.UTC)
                + datetime.timedelta(hours=1),
            },
            config.get_secret_key(),
            algorithm="HS256",
        )
        return token

    @classmethod
    def get_email_from_token(cls, token: str) -> str:
        token_payload = cls.decode_token(token)
        return token_payload["email"]

    @staticmethod
    def decode_token(token: str) -> dict:
        token_payload = jwt.decode(token, config.get_secret_key(), algorithms=["HS256"])
        return token_payload


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
