import abc
import datetime
import hashlib
from smtplib import SMTP
from uuid import uuid4, UUID

import jwt

from src import config


class TokenManager(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def generate_auth_token(username: str) -> str: ...

    @staticmethod
    @abc.abstractmethod
    def get_username_from_token(token: str) -> str: ...


class JWTManager(TokenManager):
    @staticmethod
    def generate_auth_token(username: str) -> str:
        token = jwt.encode(
            {
                "username": username,
                "exp": datetime.datetime.now(datetime.UTC)
                + datetime.timedelta(hours=1),
            },
            config.get_secret_key(),
            algorithm="HS256",
        )
        return token

    @classmethod
    def get_username_from_token(cls, token: str) -> str:
        token_payload = cls.decode_token(token)
        return token_payload["username"]

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


class Notificator(abc.ABC):
    @abc.abstractmethod
    def send_notification(self, recipient: str, subject: str, message: str) -> None: ...


class EmailNotificator(Notificator):
    def send_notification(self, recipient: str, subject: str, message: str) -> None:
        with SMTP(config.get_smtp_host()) as smtp:
            smtp.sendmail(
                from_addr=config.get_smtp_sender(),
                to_addrs=[recipient],
                msg=f"Subject: {subject}\n\n{message}".encode(),
            )


class FakeNotificator(Notificator):
    def send_notification(self, recipient: str, subject: str, message: str) -> None:
        print(f"Fake notificator: {recipient}, {subject}, {message}")
