import datetime

import pytest

from src.modules.users.domain.tokens import RefreshToken
from src.shared.application.exceptions import UserNotFound


class TestSQLAlchemyUnitOfWork:
    def test_uow_can_use_repositories(self, sqlalchemy_uow):
        with sqlalchemy_uow:
            assert sqlalchemy_uow.user_repository
            assert sqlalchemy_uow.refresh_token_repository
            assert sqlalchemy_uow.wishlist_repository

    def test_uow_persists_refresh_token(self, sqlalchemy_uow, user):
        now = datetime.datetime.now(datetime.UTC)
        refresh_token = RefreshToken(
            username=user.username,
            token_hash="token-hash",
            created_at=now,
            expires_at=now + datetime.timedelta(days=30),
        )

        with sqlalchemy_uow:
            sqlalchemy_uow.user_repository.add(user)
            sqlalchemy_uow.refresh_token_repository.add(refresh_token)
            sqlalchemy_uow.commit()

        with sqlalchemy_uow:
            stored_token = sqlalchemy_uow.refresh_token_repository.get_by_hash(
                refresh_token.token_hash
            )

        assert stored_token == refresh_token

    def test_uow_can_commit(self, sqlalchemy_uow, user):
        with sqlalchemy_uow:
            sqlalchemy_uow.user_repository.add(user)
            sqlalchemy_uow.commit()

        assert sqlalchemy_uow.user_repository.get(user.username) == user

    def test_uow_rollback_uncommitted_changes(self, sqlalchemy_uow, user):
        with sqlalchemy_uow:
            sqlalchemy_uow.user_repository.add(user)

        with pytest.raises(Exception):
            _user = sqlalchemy_uow.user_repository.get(user.username)

    def test_uow_rollback_on_error(self, sqlalchemy_uow, user):
        with pytest.raises(Exception):
            with sqlalchemy_uow:
                sqlalchemy_uow.user_repository.add(user)
                raise Exception

        with pytest.raises(UserNotFound):
            _user = sqlalchemy_uow.user_repository.get(user.username)

    def test_session_closed_on_success(self, sqlalchemy_uow, user):
        closed = []
        with sqlalchemy_uow as uow:
            real_close = uow.session.close
            uow.session.close = lambda: closed.append(True) or real_close()

        assert closed == [True]

    def test_session_closed_on_error(self, sqlalchemy_uow, user):
        closed = []
        with pytest.raises(Exception):
            with sqlalchemy_uow as uow:
                real_close = uow.session.close
                uow.session.close = lambda: closed.append(True) or real_close()
                raise Exception

        assert closed == [True]
