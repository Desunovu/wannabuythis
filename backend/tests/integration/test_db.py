import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src import config


class TestPostgres:
    @pytest.mark.skip(reason="External database dependency")
    def test_connect(self):
        session_factory = sessionmaker(bind=create_engine(config.get_postgres_uri()))
        session = session_factory()
        # Test that no OperationalError is raised
        session.execute(text("SELECT 1"))
        session.close()
