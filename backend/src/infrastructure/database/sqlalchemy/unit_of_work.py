from typing import Optional

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings
from src.infrastructure.database.sqlalchemy.repositories.user_repository import (
    SQLAlchemyUserRepository,
)
from src.infrastructure.database.sqlalchemy.repositories.wishlist_repository import (
    SQLAlchemyWishlistRepository,
)
from src.shared.application.uow import UnitOfWork


class SQLAlchemyUnitOfWork(UnitOfWork):
    _shared_engine: Optional[Engine] = None

    @classmethod
    def get_engine(cls) -> Engine:
        if cls._shared_engine is None:
            cls._shared_engine = create_engine(
                settings.postgres_uri,
            )
        return cls._shared_engine

    def __init__(self, session_factory: Optional[sessionmaker] = None):
        super().__init__()
        self.session_factory = session_factory or sessionmaker(bind=self.get_engine())

    def _commit(self):
        self.session.commit()

    def _rollback(self):
        self.session.rollback()

    def __enter__(self):
        self.session = self.session_factory()
        self.user_repository = SQLAlchemyUserRepository(self.session)
        self.wishlist_repository = SQLAlchemyWishlistRepository(self.session)
        return super().__enter__()
