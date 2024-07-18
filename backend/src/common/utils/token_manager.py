import abc
import datetime

import jwt

from src import config
from src.common.service.exceptions import TokenException


class TokenManager(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def generate_token(
        username: str, token_lifetime: None | datetime.timedelta = None
    ) -> str: ...

    @staticmethod
    @abc.abstractmethod
    def get_username_from_token(token: str) -> str: ...


class JWTManager(TokenManager):
    @staticmethod
    def generate_token(
        username: str, token_lifetime: None | datetime.timedelta = None
    ) -> str:
        payload = {"username": username}
        if token_lifetime:
            payload["exp"] = datetime.datetime.now(datetime.UTC) + token_lifetime
        token = jwt.encode(
            payload=payload,
            key=config.get_secret_key(),
            algorithm="HS256",
        )
        return token

    @staticmethod
    def __decode_token(token: str) -> dict:
        try:
            token_payload = jwt.decode(
                token,
                config.get_secret_key(),
                algorithms=["HS256"],
            )
        except jwt.exceptions.ExpiredSignatureError as e:
            raise TokenException(f"Token has expired: {token}") from e
        except jwt.exceptions.InvalidTokenError as e:
            raise TokenException(f"Invalid token: {token}") from e
        except Exception as e:
            raise TokenException(f"Unexpected error when decoding: {token}") from e
        return token_payload

    @classmethod
    def get_username_from_token(cls, token: str) -> str:
        token_payload = cls.__decode_token(token)
        return token_payload["username"]
