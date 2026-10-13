import datetime
from dataclasses import dataclass


@dataclass
class RefreshToken:
    username: str
    token_hash: str
    created_at: datetime.datetime
    expires_at: datetime.datetime
    revoked_at: datetime.datetime | None = None

    def is_revoked(self) -> bool:
        return self.revoked_at is not None

    def is_expired(self, now: datetime.datetime) -> bool:
        return self.expires_at <= now
