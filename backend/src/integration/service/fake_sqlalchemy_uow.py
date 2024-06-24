from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.integration.service.sqlalchemy_uow import SQLAlchemyUnitOfWork


class FakeSQLAlchemyUnitOfWork(SQLAlchemyUnitOfWork):
    """
    A fake implementation of SQLAlchemyUnitOfWork for testing purposes.
    This version of SQLAlchemyUnitOfWork uses an in-memory SQLite database instead of a real one.
    """

    def __init__(self):
        db_engine = create_engine("sqlite:///:memory:")
        session_factory = sessionmaker(bind=db_engine)
        super().__init__(session_factory=session_factory)
