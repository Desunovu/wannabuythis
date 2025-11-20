import logging
import time

import alembic.config
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from src.infrastructure.database.sqlalchemy.unit_of_work import SQLAlchemyUnitOfWork

logger = logging.getLogger(__name__)


def wait_for_database(max_retries: int = 10) -> None:
    """
    Wait for the database to become available.

    Raises:
        Exception: If database is not available after max_retries
    """

    for attempt in range(1, max_retries + 1):
        try:
            engine = SQLAlchemyUnitOfWork.get_engine()

            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info(f"Database connected (attempt {attempt})")
            engine.dispose()
            return
        except OperationalError as e:
            if attempt < max_retries:
                logger.warning(
                    f"Database not ready, retrying... ({attempt}/{max_retries})"
                )
                time.sleep(5)
            else:
                engine.dispose()
                raise Exception(
                    f"Database unavailable after {max_retries} attempts"
                ) from e

    engine.dispose()


def run_migrations():
    alembic_args = [
        "--raiseerr",
        "upgrade",
        "head",
    ]

    alembic.config.main(argv=alembic_args)
