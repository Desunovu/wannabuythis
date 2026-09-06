from collections.abc import Iterator

from dishka import Provider, Scope, provide
from sqlalchemy import Engine, StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.infrastructure.database.sqlalchemy.orm import mapper_registry


def create_test_sqlite_engine() -> Engine:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    mapper_registry.metadata.create_all(engine)
    return engine


class TestDatabaseProvider(Provider):
    """SQLite in-memory database for tests."""

    @provide(scope=Scope.APP)
    def get_engine(self) -> Engine:
        return create_test_sqlite_engine()

    @provide(scope=Scope.APP)
    def get_session_factory(self, engine: Engine) -> sessionmaker:
        return sessionmaker(bind=engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    def get_session(self, engine: Engine) -> Iterator[Session]:
        session_factory = sessionmaker(bind=engine, expire_on_commit=False)
        session = session_factory()
        try:
            yield session
        finally:
            session.close()
