import datetime
import logging
import os.path


def setup_logging(name) -> None:
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.DEBUG)

    # Create logs folder if it doesn't exist
    log_dir = f'{os.path.dirname(__file__) + "/../../logs"}'
    try:
        os.mkdir(log_dir)
    except FileExistsError:
        pass

    # create file handler which logs even debug messages
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    log_path = os.path.join(log_dir, f"{now}.log")
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.propagate = False
