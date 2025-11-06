from typing import Optional

from sqlalchemy import Engine, create_engine

from src.config import settings


class DatabaseManager:
    """Manages database connection and migrations"""

    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or settings.postgres_uri
        self._engine: Optional[Engine] = None

    @property
    def engine(self) -> Engine:
        """Lazy engine creation"""
        if self._engine is None:
            self._engine = create_engine(self.database_url)
        return self._engine
