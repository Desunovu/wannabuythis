import abc
import datetime

import jwt

from src import config


class TokenManager(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def generate_token(
        username: str, exp_time: None | datetime.timedelta = None
    ) -> str: ...

    @staticmethod
    @abc.abstractmethod
    def get_username_from_token(token: str) -> str: ...


class JWTManager(TokenManager):
    @staticmethod
    def generate_token(
        username: str, exp_time: None | datetime.timedelta = None
    ) -> str:
        payload = {"username": username}
        if exp_time:
            payload["exp"] = datetime.datetime.now(datetime.UTC) + exp_time
        token = jwt.encode(
            payload=payload,
            key=config.get_secret_key(),
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
