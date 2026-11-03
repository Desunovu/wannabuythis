import abc
import datetime

from src.modules.users.domain.tokens import RefreshToken


class RefreshTokenRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, refresh_token: RefreshToken) -> None: ...

    @abc.abstractmethod
    def get_by_hash(self, token_hash: str) -> RefreshToken | None: ...

    @abc.abstractmethod
    def revoke(self, token_hash: str, revoked_at: datetime.datetime) -> None: ...

    @abc.abstractmethod
    def revoke_if_active(
        self, token_hash: str, revoked_at: datetime.datetime
    ) -> bool: ...

    @abc.abstractmethod
    def revoke_all_for_user(
        self, username: str, revoked_at: datetime.datetime
    ) -> None: ...


class FakeRefreshTokenRepository(RefreshTokenRepository):
    """In-memory implementation for unit tests."""

    def __init__(self):
        self._tokens: dict[str, RefreshToken] = {}

    def add(self, refresh_token: RefreshToken) -> None:
        self._tokens[refresh_token.token_hash] = refresh_token

    def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        return self._tokens.get(token_hash)

    def revoke(self, token_hash: str, revoked_at: datetime.datetime) -> None:
        refresh_token = self._tokens.get(token_hash)
        if refresh_token is not None and not refresh_token.is_revoked():
            refresh_token.revoked_at = revoked_at

    def revoke_if_active(self, token_hash: str, revoked_at: datetime.datetime) -> bool:
        refresh_token = self._tokens.get(token_hash)
        if (
            refresh_token is None
            or refresh_token.is_revoked()
            or refresh_token.is_expired(revoked_at)
        ):
            return False
        refresh_token.revoked_at = revoked_at
        return True

    def revoke_all_for_user(self, username: str, revoked_at: datetime.datetime) -> None:
        for refresh_token in self._tokens.values():
            if refresh_token.username == username and not refresh_token.is_revoked():
                refresh_token.revoked_at = revoked_at
