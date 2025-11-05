from typing import Optional

from src.config import settings


class DatabaseManager:
    """Manages database connection and migrations"""

    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or settings.postgres_uri
