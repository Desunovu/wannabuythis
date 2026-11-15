# pyright: reportUnusedCallResult=false, reportAny=false

import datetime
from typing import final, override

from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from src.infrastructure.database.sqlalchemy.orm import refresh_tokens
from src.modules.users.domain.tokens import RefreshToken
from src.modules.users.infrastructure.refresh_token_repository import (
    RefreshTokenRepository,
)


@final
class SQLAlchemyRefreshTokenRepository(RefreshTokenRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    @override
    def add(self, refresh_token: RefreshToken) -> None:
        self.session.execute(
            insert(refresh_tokens).values(
                token_hash=refresh_token.token_hash,
                username=refresh_token.username,
                created_at=refresh_token.created_at,
                expires_at=refresh_token.expires_at,
                revoked_at=refresh_token.revoked_at,
            )
        )

    @override
    def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        row = (
            self.session.execute(
                select(refresh_tokens).where(refresh_tokens.c.token_hash == token_hash)
            )
            .mappings()
            .first()
        )
        if row is None:
            return None
        return RefreshToken(
            username=row["username"],
            token_hash=row["token_hash"],
            created_at=row["created_at"],
            expires_at=row["expires_at"],
            revoked_at=row["revoked_at"],
        )

    @override
    def revoke(self, token_hash: str, revoked_at: datetime.datetime) -> None:
        self.session.execute(
            update(refresh_tokens)
            .where(
                refresh_tokens.c.token_hash == token_hash,
                refresh_tokens.c.revoked_at.is_(None),
            )
            .values(revoked_at=revoked_at)
        )

    @override
    def revoke_if_active(self, token_hash: str, revoked_at: datetime.datetime) -> bool:
        revoked = self.session.execute(
            update(refresh_tokens)
            .where(
                refresh_tokens.c.token_hash == token_hash,
                refresh_tokens.c.revoked_at.is_(None),
                refresh_tokens.c.expires_at > revoked_at,
            )
            .values(revoked_at=revoked_at)
            .returning(refresh_tokens.c.token_hash)
        )
        return revoked.first() is not None

    @override
    def revoke_all_for_user(self, username: str, revoked_at: datetime.datetime) -> None:
        self.session.execute(
            update(refresh_tokens)
            .where(
                refresh_tokens.c.username == username,
                refresh_tokens.c.revoked_at.is_(None),
            )
            .values(revoked_at=revoked_at)
        )
