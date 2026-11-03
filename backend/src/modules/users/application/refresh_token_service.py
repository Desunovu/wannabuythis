import datetime
import hashlib
import secrets

from src.modules.users.application.dto import IssuedRefreshToken
from src.modules.users.domain.tokens import RefreshToken


class RefreshTokenService:
    @staticmethod
    def hash_token(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    def issue(self, username: str, lifetime: datetime.timedelta) -> IssuedRefreshToken:
        raw_token = secrets.token_urlsafe(32)
        created_at = datetime.datetime.now(datetime.UTC)
        record = RefreshToken(
            username=username,
            token_hash=self.hash_token(raw_token),
            created_at=created_at,
            expires_at=created_at + lifetime,
        )
        return IssuedRefreshToken(raw_token=raw_token, record=record)
