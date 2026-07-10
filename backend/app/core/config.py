from __future__ import annotations

from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import AliasChoices, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    _project_root = Path(__file__).resolve().parents[3]

    model_config = SettingsConfigDict(
        env_file=(_project_root / ".env", _project_root / "backend" / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        validate_default=True,
    )

    environment: Environment = Field(
        default=Environment.DEVELOPMENT,
        validation_alias=AliasChoices("APP_ENV", "ENVIRONMENT"),
    )
    debug: bool | None = Field(default=None, validation_alias="DEBUG")
    api_v1_prefix: str = Field(
        default="/api/v1",
        validation_alias="API_V1_PREFIX",
    )
    database_url: str | None = Field(default=None, validation_alias="DATABASE_URL")
    redis_url: str | None = Field(default=None, validation_alias="REDIS_URL")
    cors_origins: list[str] | None = Field(
        default=None,
        validation_alias="CORS_ORIGINS",
    )
    log_level: str | None = Field(default=None, validation_alias="LOG_LEVEL")
    supabase_url: str | None = Field(default=None, validation_alias="SUPABASE_URL")
    supabase_publishable_key: str | None = Field(
        default=None,
        validation_alias="SUPABASE_PUBLISHABLE_KEY",
    )
    supabase_jwks_url: str | None = Field(
        default=None,
        validation_alias="SUPABASE_JWKS_URL",
    )
    supabase_jwt_audience: str | None = Field(
        default=None,
        validation_alias="SUPABASE_JWT_AUDIENCE",
    )
    gemini_api_key: str | None = Field(default=None, validation_alias="GEMINI_API_KEY")
    vertex_project_id: str | None = Field(
        default=None,
        validation_alias="VERTEX_PROJECT_ID",
    )
    vertex_location: str | None = Field(default=None, validation_alias="VERTEX_LOCATION")

    @field_validator("api_v1_prefix")
    @classmethod
    def validate_api_prefix(cls, value: str) -> str:
        prefix = value.strip()
        if not prefix:
            raise ValueError("API_V1_PREFIX cannot be empty.")
        if not prefix.startswith("/"):
            raise ValueError("API_V1_PREFIX must start with '/'.")
        if prefix != "/" and prefix.endswith("/"):
            prefix = prefix.rstrip("/")
        return prefix

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip().upper()
        allowed_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if normalized not in allowed_levels:
            raise ValueError(
                "LOG_LEVEL must be one of DEBUG, INFO, WARNING, ERROR, or CRITICAL."
            )
        return normalized

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug_flag(cls, value: Any) -> bool | None:
        if value is None or value == "":
            return None
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            truthy = {"1", "true", "yes", "on", "debug", "development", "dev"}
            falsy = {
                "0",
                "false",
                "no",
                "off",
                "release",
                "production",
                "prod",
                "test",
                "testing",
            }
            if normalized in truthy:
                return True
            if normalized in falsy:
                return False
        raise ValueError(
            "DEBUG must be a boolean or one of: true, false, yes, no, on, off, debug, "
            "development, release, production, prod, test, testing."
        )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> list[str] | None:
        if value is None or value == "":
            return None
        if isinstance(value, str):
            items = [item.strip() for item in value.split(",")]
        elif isinstance(value, (list, tuple, set)):
            items = [str(item).strip() for item in value]
        else:
            raise ValueError("CORS_ORIGINS must be a comma-separated string or a list.")

        origins = [item.rstrip("/") for item in items if item]
        for origin in origins:
            if not origin.startswith(("http://", "https://")):
                raise ValueError(
                    "CORS_ORIGINS entries must start with http:// or https://."
                )
        return origins or None

    @field_validator(
        "database_url",
        "redis_url",
        "supabase_url",
        "supabase_publishable_key",
        "supabase_jwks_url",
        "supabase_jwt_audience",
        "gemini_api_key",
        "vertex_project_id",
        "vertex_location",
        mode="before",
    )
    @classmethod
    def empty_strings_to_none(cls, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            stripped = value.strip()
            return stripped or None
        return value

    @model_validator(mode="after")
    def apply_environment_defaults(self) -> "Settings":
        if self.debug is None:
            self.debug = self.environment is not Environment.PRODUCTION

        if self.log_level is None:
            self.log_level = (
                "DEBUG"
                if self.environment is not Environment.PRODUCTION
                else "INFO"
            )

        if self.cors_origins is None:
            self.cors_origins = (
                ["http://localhost:8080"]
                if self.environment is not Environment.PRODUCTION
                else []
            )

        if self.database_url is None:
            if self.environment is Environment.PRODUCTION:
                raise ValueError("DATABASE_URL is required in production.")
            if self.environment is Environment.TESTING:
                self.database_url = "sqlite+pysqlite:///:memory:"
            else:
                self.database_url = "sqlite+pysqlite:///./decision_iq.db"

        if self.redis_url is None:
            if self.environment is Environment.PRODUCTION:
                raise ValueError("REDIS_URL is required in production.")
            if self.environment is Environment.TESTING:
                self.redis_url = "redis://localhost:6379/15"
            else:
                self.redis_url = "redis://localhost:6379/0"

        if self.environment is Environment.PRODUCTION:
            missing = [
                name
                for name, value in {
                    "SUPABASE_URL": self.supabase_url,
                    "SUPABASE_PUBLISHABLE_KEY": self.supabase_publishable_key,
                }.items()
                if value is None
            ]
            if missing:
                raise ValueError(
                    f"Missing required production settings: {', '.join(missing)}"
                )
            if self.debug:
                raise ValueError("DEBUG must be disabled in production.")

        if self.supabase_jwks_url is None and self.supabase_url is not None:
            base_url = self.supabase_url.rstrip("/")
            self.supabase_jwks_url = f"{base_url}/auth/v1/.well-known/jwks.json"

        if (
            self.supabase_jwt_audience is None
            and self.environment is not Environment.TESTING
        ):
            self.supabase_jwt_audience = "authenticated"

        return self

    @property
    def is_development(self) -> bool:
        return self.environment is Environment.DEVELOPMENT

    @property
    def is_testing(self) -> bool:
        return self.environment is Environment.TESTING

    @property
    def is_production(self) -> bool:
        return self.environment is Environment.PRODUCTION


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
