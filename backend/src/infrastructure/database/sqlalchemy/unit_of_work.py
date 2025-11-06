from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings
from src.infrastructure.database.sqlalchemy.repositories.user_repository import \
    SQLAlchemyUserRepository
from src.infrastructure.database.sqlalchemy.repositories.wishlist_repository import \
    SQLAlchemyWishlistRepository
from src.shared.application.uow import UnitOfWork


class SQLAlchemyUnitOfWork(UnitOfWork):
    DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(settings.postgres_uri))

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
