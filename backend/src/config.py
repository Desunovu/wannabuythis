import datetime
import secrets
from functools import lru_cache
from typing import Annotated, Literal, Self

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # Environment
    env: Literal["development", "production", "testing"] = Field(
        default="development",
        description="Application environment",
    )

    # Database configuration
    postgres_user: str = Field(default="postgres", description="PostgreSQL username")
    postgres_password: str = Field(
        default="postgres", description="PostgreSQL password"
    )
    postgres_host: str = Field(default="localhost", description="PostgreSQL host")
    postgres_port: int = Field(default=5432, description="PostgreSQL port")
    postgres_db: str = Field(default="postgres", description="PostgreSQL database name")

    # Security
    secret_key: str | None = Field(
        default=None,
        min_length=32,
        description=(
            "Secret key for JWT authentication. Required in production; "
            "generated randomly in development."
        ),
    )

    # SMTP configuration
    smtp_host: str = Field(default="localhost", description="SMTP server host")
    smtp_port: int = Field(default=25, description="SMTP server port")
    smtp_sender: str = Field(
        default="admin@localhost", description="Email sender address"
    )
    smtp_username: str | None = Field(
        default=None, description="SMTP authentication username"
    )
    smtp_password: str | None = Field(
        default=None, description="SMTP authentication password"
    )
    smtp_use_tls: bool = Field(default=False, description="Use TLS for SMTP")

    # Application
    base_url: str = Field(
        default="http://localhost:8000",
        description="Base URL of the application",
    )

    # CORS
    cors_allow_origins: Annotated[list[str], NoDecode] = Field(
        default_factory=list,
        description="Comma-separated browser origins; empty disables cross-origin",
    )

    # Token lifetimes
    access_token_lifetime_in_minutes: int = Field(
        default=15,
        ge=1,
        le=60,
        description="Access token lifetime in minutes",
    )
    refresh_token_lifetime_in_days: int = Field(
        default=30,
        ge=1,
        le=365,
        description="Refresh token lifetime in days",
    )
    activation_token_lifetime_in_hours: int = Field(
        default=24,
        ge=1,
        le=168,
        description="Activation token lifetime in hours",
    )
    email_change_code_lifetime_in_minutes: int = Field(
        default=60,
        ge=1,
        le=1440,
        description="Email change code lifetime in minutes",
    )

    # Redis configuration
    redis_host: str = Field(default="localhost", description="Redis host")
    redis_port: int = Field(default=6379, description="Redis port")
    redis_activation_codes_db: int = Field(
        default=0,
        ge=0,
        le=15,
        description="Redis activation codes database",
    )
    redis_password: str | None = Field(default=None, description="Redis password")

    # Rate limiting
    rate_limit_storage_uri: str | None = Field(
        default=None, description="Rate limiter storage URI; null means in-memory"
    )

    # User name validation
    users_name_min_length: int = Field(
        default=3, description="Minimum length of username"
    )
    users_name_max_length: int = Field(
        default=29, description="Maximum length of username"
    )
    users_forbidden_names: set[str] = Field(
        default=(
            "admin",
            "root",
            "superuser",
            "moderator",
            "test",
            "invalid",
            "profile",
            "login",
            "user",
            "users",
        ),
        description="Set of forbidden names",
    )

    # Wishlist validation
    wishlists_name_max_length: int = Field(
        default=255, ge=1, description="Maximum length of wishlist name"
    )
    wishlists_item_name_max_length: int = Field(
        default=255, ge=1, description="Maximum length of wishlist item name"
    )
    wishlists_item_quantity_max: int = Field(
        default=1_000, ge=1, description="Maximum quantity per wishlist item"
    )
    wishlists_items_max_count: int = Field(
        default=100,
        ge=1,
        le=10_000,
        description="Maximum number of items in a wishlist",
    )

    # Pagination
    wishlists_pagination_default_size: int = Field(
        default=20,
        ge=1,
        description="Default page size of wishlist list endpoints",
    )
    wishlists_pagination_max_size: int = Field(
        default=100,
        ge=1,
        le=1_000,
        description="Maximum page size of wishlist list endpoints",
    )

    # Computed properties
    @property
    def postgres_uri(self) -> str:
        """Generate PostgreSQL connection URI."""
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def access_token_lifetime(self) -> datetime.timedelta:
        """Get access token lifetime as timedelta."""
        return datetime.timedelta(minutes=self.access_token_lifetime_in_minutes)

    @property
    def refresh_token_lifetime(self) -> datetime.timedelta:
        """Get refresh token lifetime as timedelta."""
        return datetime.timedelta(days=self.refresh_token_lifetime_in_days)

    @property
    def activation_code_lifetime(self) -> datetime.timedelta:
        """Get activation code lifetime as timedelta."""
        return datetime.timedelta(hours=self.activation_token_lifetime_in_hours)

    @property
    def email_change_code_lifetime(self) -> datetime.timedelta:
        """Get email change code lifetime as timedelta."""
        return datetime.timedelta(minutes=self.email_change_code_lifetime_in_minutes)

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.env == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.env == "development"

    @property
    def is_testing(self) -> bool:
        """Check if running in testing environment."""
        return self.env == "testing"

    @property
    def jwt_secret_key(self) -> str:
        """Resolved JWT signing key, never None after validation."""
        assert self.secret_key is not None
        return self.secret_key

    @model_validator(mode="after")
    def ensure_secret_key(self) -> Self:
        """Require an explicit key in production, generate a random one otherwise."""
        if self.secret_key is None:
            if self.env == "production":
                raise ValueError(
                    "SECRET_KEY must be set to a secure value in production environment"
                )
            self.secret_key = secrets.token_urlsafe(48)
        return self

    @model_validator(mode="after")
    def ensure_pagination_limits(self) -> Self:
        """Keep the default page size within the allowed maximum."""
        if self.wishlists_pagination_default_size > self.wishlists_pagination_max_size:
            raise ValueError(
                "WISHLISTS_PAGINATION_DEFAULT_SIZE must not exceed "
                + "WISHLISTS_PAGINATION_MAX_SIZE"
            )
        return self

    @field_validator("base_url")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        """Ensure base URL doesn't end with a slash."""
        return v.rstrip("/")

    @field_validator("cors_allow_origins", mode="before")
    @classmethod
    def split_cors_allow_origins(cls, v):
        """Turn the comma-separated env value into a list of origins."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v


# Settings have two access paths: this module-level instance is read at import
# time for declarative constraints (Pydantic schemas, FastAPI Query/OpenAPI),
# where values must be known before the DI container exists; SettingsProvider
# serves the same instance to runtime code. Keep runtime code on injection and
# import this global only for import-time declarations.
@lru_cache
def get_settings() -> Settings:
    """Get cached application settings"""
    return Settings()


settings = get_settings()
