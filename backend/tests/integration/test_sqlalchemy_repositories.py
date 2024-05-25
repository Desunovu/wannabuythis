from src.common.adapters.dependencies import DefaultPasswordManager
from src.integration.adapters.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.users.domain.user import User


class TestSQLAlchemyUserRepository:
    def test_get_user(self, sqlite_session, user):
        sqlite_session.add(user)
        sqlite_session.commit()
        repository = SQLAlchemyUserRepository(sqlite_session)
        assert repository.get(user.username) is not None

    def test_get_non_existing_user(self, sqlite_session):
        repository = SQLAlchemyUserRepository(sqlite_session)
        assert repository.get("testuser") is None

    def test_add_user(self, sqlite_session, user):
        repository = SQLAlchemyUserRepository(sqlite_session)
        repository.add(user)
        assert repository.get(user.username) is not None
