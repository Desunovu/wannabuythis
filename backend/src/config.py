import os
import datetime


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


# Selector of production vs. development environment
def get_env() -> str:
    return os.environ.get("ENV", "development")


def get_base_url() -> str:
    return os.environ.get("BASE_URL", "http://localhost:8000")


def get_auth_token_lifetime() -> datetime.timedelta:
    token_lifetime_in_hours = os.environ.get("TOKEN_LIFETIME_IN_HOURS", "24")
    return datetime.timedelta(hours=int(token_lifetime_in_hours))


def get_activation_token_lifetime() -> datetime.timedelta:
    token_lifetime_in_hours = os.environ.get("ACTIVATION_TOKEN_LIFETIME_IN_HOURS", "24")
    return datetime.timedelta(hours=int(token_lifetime_in_hours))
