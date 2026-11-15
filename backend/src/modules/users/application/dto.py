from dataclasses import dataclass

from src.modules.users.domain.tokens import RefreshToken


@dataclass(frozen=True)
class TokenPair:
    access_token: str
    refresh_token: str


@dataclass(frozen=True)
class IssuedRefreshToken:
    raw_token: str
    record: RefreshToken
