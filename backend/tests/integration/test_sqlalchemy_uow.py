import pytest


class TestSQLAlchemyUnitOfWork:
    def test_uow_can_use_repositories(self, sqlalchemy_uow):
        with sqlalchemy_uow:
            assert sqlalchemy_uow.user_repository
            assert sqlalchemy_uow.wishlist_repository

    def test_uow_can_commit(self, sqlalchemy_uow, user):
        with sqlalchemy_uow:
            sqlalchemy_uow.user_repository.add(user)
            sqlalchemy_uow.commit()

        assert sqlalchemy_uow.user_repository.get(user.username) == user

    def test_uow_rollback_uncommitted_changes(self, sqlalchemy_uow, user):
        with sqlalchemy_uow:
            sqlalchemy_uow.user_repository.add(user)

        assert sqlalchemy_uow.user_repository.get(user.username) is None

    def test_uow_rollback_on_error(self, sqlalchemy_uow, user):
        with pytest.raises(Exception):
            with sqlalchemy_uow:
                sqlalchemy_uow.user_repository.add(user)
                raise Exception

        assert sqlalchemy_uow.user_repository.get(user.username) is None
