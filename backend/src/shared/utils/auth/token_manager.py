import abc
import datetime
from typing import override

import jwt

from src.config import Settings
from src.shared.application.exceptions import TokenException


class TokenManager(abc.ABC):
    @abc.abstractmethod
    def generate_token(
        self, username: str, token_lifetime: None | datetime.timedelta = None
    ) -> str: ...

    @abc.abstractmethod
    def get_username_from_token(self, token: str) -> str: ...


class JWTManager(TokenManager):
    def __init__(self, settings: Settings):
        self._secret_key: str = settings.secret_key

    @override
    def generate_token(
        self, username: str, token_lifetime: None | datetime.timedelta = None
    ) -> str:
        payload = {"username": username}
        if token_lifetime:
            payload["exp"] = datetime.datetime.now(datetime.UTC) + token_lifetime
        token = jwt.encode(
            payload=payload,
            key=self._secret_key,
            algorithm="HS256",
        )
        return token

    @override
    def get_username_from_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError as e:
            raise TokenException("Token expired") from e
        except jwt.InvalidTokenError as e:
            raise TokenException("Invalid token") from e
        return payload["username"]
