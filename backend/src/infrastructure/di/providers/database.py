from typing import Iterable

from dishka import Provider, Scope, provide
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import Settings


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_engine(self, settings: Settings) -> Engine:
        return create_engine(settings.postgres_uri)

    @provide(scope=Scope.APP)
    def get_session_factory(self, engine: Engine) -> sessionmaker:
        return sessionmaker(bind=engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    def get_session(self, session_factory: sessionmaker) -> Iterable[Session]:
        session = session_factory()
        try:
            yield session
        finally:
            session.close()
