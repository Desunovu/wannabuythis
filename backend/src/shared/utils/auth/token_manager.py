import abc
import datetime
from dataclasses import dataclass
from typing import override

import jwt

from src.config import Settings
from src.shared.application.exceptions import TokenException

ACCESS_TOKEN_TYPE = "access"


@dataclass(frozen=True)
class AccessTokenPayload:
    username: str
    issued_at: datetime.datetime
    expires_at: datetime.datetime


class TokenManager(abc.ABC):
    @abc.abstractmethod
    def create_access_token(
        self, username: str, token_lifetime: datetime.timedelta
    ) -> str: ...

    @abc.abstractmethod
    def decode_token(self, token: str) -> AccessTokenPayload: ...


class JWTManager(TokenManager):
    def __init__(self, settings: Settings):
        self._secret_key: str = settings.jwt_secret_key

    @override
    def create_access_token(
        self, username: str, token_lifetime: datetime.timedelta
    ) -> str:
        now = datetime.datetime.now(datetime.UTC)
        payload = {
            "sub": username,
            "type": ACCESS_TOKEN_TYPE,
            "iat": now.timestamp(),
            "exp": (now + token_lifetime).timestamp(),
        }
        token = jwt.encode(
            payload=payload,
            key=self._secret_key,
            algorithm="HS256",
        )
        return token

    @override
    def decode_token(self, token: str) -> AccessTokenPayload:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError as e:
            raise TokenException("Token expired") from e
        except jwt.InvalidTokenError as e:
            raise TokenException("Invalid token") from e

        if payload.get("type") != ACCESS_TOKEN_TYPE:
            raise TokenException("Invalid token type")

        return AccessTokenPayload(
            username=payload["sub"],
            issued_at=datetime.datetime.fromtimestamp(payload["iat"], datetime.UTC),
            expires_at=datetime.datetime.fromtimestamp(payload["exp"], datetime.UTC),
        )
