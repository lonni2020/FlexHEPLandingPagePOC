"""Application configuration loaded from the local environment."""

import logging
from typing import Any

from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from python_sentry_logger_wrapper import get_logger

# =============================================================================
# CONFIGURATION - Modify these values for your project
# =============================================================================
DEFAULT_APP_NAME = "FlexHEP"
DEFAULT_APP_VERSION = "0.1.0"
# =============================================================================


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Environment variables are case-insensitive.
    Values are loaded from (in order of precedence):
    1. Environment variables
    2. .env file
    3. Default values defined here
    """

    # -------------------------------------------------------------------------
    # API Settings
    # -------------------------------------------------------------------------
    app_name: str = DEFAULT_APP_NAME
    app_version: str = DEFAULT_APP_VERSION

    # -------------------------------------------------------------------------
    # Environment Settings
    # -------------------------------------------------------------------------
    environment: str = "development"
    log_level: str = "info"

    # -------------------------------------------------------------------------
    # Database Settings
    # -------------------------------------------------------------------------
    database_url: str = "sqlite+aiosqlite:///./data/flexhep.db"

    test_database_url: str = "sqlite+aiosqlite:///./data/flexhep-test.db"

    # -------------------------------------------------------------------------
    # Sentry Settings (Optional - for error tracking and monitoring)
    # -------------------------------------------------------------------------
    sentry_dsn: str | None = None
    sentry_environment: str | None = None
    sentry_sample_rate: float = 1.0  # Sample all traces by default
    sentry_send_pii: bool = False  # Never send PII by default
    sentry_breadcrumbs_level: str | None = None
    sentry_log_level: str | None = None

    # -------------------------------------------------------------------------
    # Logger (initialized after settings are loaded)
    # -------------------------------------------------------------------------
    logger: Any | None = None

    # -------------------------------------------------------------------------
    # Pydantic Configuration
    # -------------------------------------------------------------------------
    model_config = ConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,  # Allow UPPER_CASE env vars to map to lower_case fields
        extra="ignore",  # Ignore unknown environment variables
    )


# Create singleton instance - imported throughout the application
settings = Settings()

# Initialize logger with Sentry integration
log_level_map = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}

log_level = log_level_map.get(settings.log_level.lower(), logging.INFO)
sentry_log_level = (
    log_level_map.get(settings.sentry_log_level.lower(), logging.INFO)
    if settings.sentry_log_level
    else logging.INFO
)
sentry_breadcrumbs_level = (
    log_level_map.get(settings.sentry_breadcrumbs_level.lower(), logging.ERROR)
    if settings.sentry_breadcrumbs_level
    else logging.ERROR
)

settings.logger = get_logger(
    service_name=settings.app_name,
    log_level=log_level,
    sentry_dsn=settings.sentry_dsn,
    sentry_breadcrumbs_level=sentry_breadcrumbs_level,
    sentry_logs_level=sentry_log_level,
    sentry_environment=settings.sentry_environment,
    traces_sample_rate=settings.sentry_sample_rate,
    sentry_send_pii=settings.sentry_send_pii,
)

# Environment constants for consistent checks across codebase
LOCAL_ENVIRONMENTS = ("local", "development", "dev")
