import enum
from functools import lru_cache
from typing import List, Union

from pydantic import AnyHttpUrl, ConfigDict, field_validator
from pydantic_settings import BaseSettings


class AppENV(enum.Enum):
    LOCAL = "local"
    DEV = "dev"
    STG = "stg"
    PROD = "prod"


class Settings(BaseSettings):
    model_config = ConfigDict(case_sensitive=True, env_file_encoding="utf-8")

    ENV: AppENV = AppENV.LOCAL
    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    OPENAPI_URL: str = f"{API_V1_STR}/openapi.json"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # JWT Configuration - MUST be set in environment variables for production
    JWT_SECRET: str
    ALGORITHM: str = "HS256"
    # 60 minutes * 8 hours
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8

    # Timezone configuration
    TIMEZONE: str = "UTC"

    # Rate Limiting Configuration
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60
    RATE_LIMIT_AUTH_REQUESTS_PER_MINUTE: int = 5
    RATE_LIMIT_BURST_SIZE: int = 10

    # Security Configuration
    ENABLE_REQUEST_LOGGING: bool = True
    ENABLE_INPUT_VALIDATION: bool = True
    ENABLE_SECURITY_HEADERS: bool = True

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @field_validator("JWT_SECRET")
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        if not v:
            raise ValueError("JWT_SECRET is required")
        if len(v) < 32:
            raise ValueError("JWT_SECRET should be at least 32 characters long")
        return v

    # For DB
    DB_HOST: str
    DB_PORT: str = "5432"
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    DB_SOCKET_DIR: str = "/cloudsql"
    DB_INSTANCE_NAME: str = "<YOUR_INSTANCE_NAME>"


@lru_cache()
def get_settings():
    settings = Settings(_env_file=".env")
    return settings


settings = get_settings()
