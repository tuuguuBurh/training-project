from enum import Enum
from functools import lru_cache

from pydantic import AnyHttpUrl, Field, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppENV(str, Enum):
    """Application environment enumeration."""

    LOCAL = "local"
    DEV = "dev"
    STG = "stg"
    PROD = "prod"

    @property
    def is_production(self) -> bool:
        return self in (AppENV.STG, AppENV.PROD)

    @property
    def is_development(self) -> bool:
        return self in (AppENV.LOCAL, AppENV.DEV)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Application ---
    ENV: AppENV = Field(default=AppENV.LOCAL, description="Current application environment")
    PROJECT_NAME: str = Field(..., description="Name of the project")
    API_V1_STR: str = Field(default="/api/v1", description="API version prefix")

    # --- CORS ---
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = Field(default=[], description="Allowed CORS origins")

    # --- JWT Configuration ---
    JWT_SECRET: str = Field(..., min_length=32, description="Secret key for JWT generation")
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60 * 8, description="Access token expiration in minutes (default 8h)"
    )

    # --- Timezone & Localization ---
    TIMEZONE: str = Field(default="UTC", description="Application timezone")

    # --- Rate Limiting ---
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = Field(default=60, description="Global rate limit")
    RATE_LIMIT_AUTH_REQUESTS_PER_MINUTE: int = Field(default=5, description="Auth-specific rate limit")
    RATE_LIMIT_BURST_SIZE: int = Field(default=10, description="Burst size for token bucket")

    # --- Feature Toggles ---
    ENABLE_REQUEST_LOGGING: bool = Field(default=True, description="Enable per-request logging")
    ENABLE_INPUT_VALIDATION: bool = Field(default=True, description="Enable extra input validation")
    ENABLE_SECURITY_HEADERS: bool = Field(default=True, description="Enable security headers middleware")

    # --- Database ---
    DB_HOST: str = Field(..., description="Database host")
    DB_PORT: int = Field(default=5432, description="Database port")
    DB_USER: str = Field(..., description="Database username")
    DB_PASS: str = Field(..., description="Database password")
    DB_NAME: str = Field(..., description="Database name")
    DB_SOCKET_DIR: str = Field(default="/cloudsql", description="Unix socket directory for Cloud SQL")
    DB_INSTANCE_NAME: str = Field(default="", description="Cloud SQL instance connection name")

    @computed_field
    @property
    def OPENAPI_URL(self) -> str | None:
        """Disable OpenAPI in production environments."""
        if self.ENV.is_production:
            return None
        return f"{self.API_V1_STR}/openapi.json"

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """Construct database connection URL."""
        # For local development with socket or host
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        """Parse CORS origins from comma-separated string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
