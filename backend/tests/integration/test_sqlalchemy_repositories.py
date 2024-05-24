from src.common.adapters.dependencies import DefaultPasswordManager
from src.integration.adapters.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.users.domain.user import User


class TestSQLAlchemyUserRepository:
    def test_get_user(self, sqlite_session_factory):
        session = sqlite_session_factory()
        user = User(
            username="testuser", email="testemail@example.com", password_hash="password"
        )
        session.add(user)
        session.commit()
        repository = SQLAlchemyUserRepository(session=session)
        assert repository.get("testuser") is not None

    def test_get_non_existing_user(self, sqlite_session_factory):
        session = sqlite_session_factory()
        repository = SQLAlchemyUserRepository(session=session)
        assert repository.get("testuser") is None

    def test_add_user(self, sqlite_session_factory):
        session = sqlite_session_factory()
        repository = SQLAlchemyUserRepository(session=session)
        user = User(
            username="testuser", email="testemail@example.com", password_hash="password"
        )
        repository.add(user)
        assert repository.get("testuser") is not None
