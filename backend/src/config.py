import os


def get_postgres_uri() -> str:
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "postgres")
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    db = os.environ.get("POSTGRES_DB", "postgres")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


def get_secret_key() -> str:
    return os.environ.get("SECRET_KEY", "dev-secret-key")


def get_smtp_host() -> str:
    return os.environ.get("SMTP_HOST", "localhost")


def get_smtp_sender() -> str:
    return os.environ.get("SMTP_SENDER", "admin@localhost")
