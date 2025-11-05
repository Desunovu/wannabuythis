import datetime
from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    secret_key: str = Field(
        default="dev-secret-key",
        min_length=14,
        description="Secret key for JWT authentication",
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

    # Token lifetimes
    token_lifetime_in_hours: int = Field(
        default=24,
        ge=1,
        le=720,
        description="Auth token lifetime in hours",
    )
    activation_token_lifetime_in_hours: int = Field(
        default=24,
        ge=1,
        le=168,
        description="Activation token lifetime in hours",
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

    # Computed properties
    @property
    def postgres_uri(self) -> str:
        """Generate PostgreSQL connection URI."""
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def auth_token_lifetime(self) -> datetime.timedelta:
        """Get auth token lifetime as timedelta."""
        return datetime.timedelta(hours=self.token_lifetime_in_hours)

    @property
    def activation_token_lifetime(self) -> datetime.timedelta:
        """Get activation token lifetime as timedelta."""
        return datetime.timedelta(hours=self.activation_token_lifetime_in_hours)

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

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str, info) -> str:
        """Validate secret key in production."""
        if info.data.get("env") == "production" and v == "dev-secret-key":
            raise ValueError(
                "SECRET_KEY must be set to a secure value in production environment"
            )
        return v

    @field_validator("base_url")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        """Ensure base URL doesn't end with a slash."""
        return v.rstrip("/")


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings"""
    return Settings()


settings = get_settings()
