from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src import config
from src.common.service.uow import UnitOfWork
from src.integration.adapters.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.integration.adapters.sqlalchemy_wishlist_repository import (
    SQLAlchemyWishlistRepository,
)


class SQLAlchemyUnitOfWork(UnitOfWork):
    DEFAULT_SESSION_FACTORY = sessionmaker(
        bind=create_engine(config.get_postgres_uri())
    )

    def __init__(self, session_factory: sessionmaker = DEFAULT_SESSION_FACTORY):
        super().__init__()
        self.session_factory = session_factory

    def _commit(self):
        self.session.commit()

    def _rollback(self):
        self.session.rollback()

    def __enter__(self):
        self.session = self.session_factory()
        self.user_repository = SQLAlchemyUserRepository(self.session)
        self.wishlist_repository = SQLAlchemyWishlistRepository(self.session)
        return super().__enter__()
