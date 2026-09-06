import logging
import time

import alembic.config
from sqlalchemy import Engine, text
from sqlalchemy.exc import OperationalError

logger = logging.getLogger(__name__)


def wait_for_database(engine: Engine, max_retries: int = 10) -> None:
    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info(f"Database connected (attempt {attempt})")
            return
        except OperationalError:
            if attempt < max_retries:
                logger.warning(f"Retrying... ({attempt}/{max_retries})")
                time.sleep(5)
            else:
                raise Exception(f"Database unavailable after {max_retries} attempts")


def run_migrations():
    alembic_args = [
        "--raiseerr",
        "upgrade",
        "head",
    ]

    alembic.config.main(argv=alembic_args)
