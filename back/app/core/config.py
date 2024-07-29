from functools import lru_cache
from typing import List, Union

from pydantic import AnyHttpUrl, ConfigDict, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(case_sensitive=True, env_file_encoding="utf-8")

    ENV: str = "local"
    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    OPENAPI_URL: str = f"{API_V1_STR}/openapi.json"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    DOMAIN: str

    # Generate random string in production environment
    JWT_SECRET: str = "TEST_SECRET_DO_NOT_USE_IN_PROD"
    ALGORITHM: str = "HS256"
    # 60 minutes * 8 hours
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # For DB
    DB_HOST: str
    DB_PORT: str = "5432"
    DB_USER: str
    DB_PASS: str
    DB_NAME: str


@lru_cache()
def get_settings():
    settings = Settings(_env_file=".env")

    return settings


settings = get_settings()
