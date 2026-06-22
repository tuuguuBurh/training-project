import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.middlewares.db_session import DBSessionMiddleware
from app.middlewares.input_validation import InputValidationMiddleware
from app.middlewares.rate_limit import RateLimitMiddleware
from app.middlewares.request_logging import RequestLoggingMiddleware
from app.middlewares.security_headers import SecurityHeadersMiddleware
from app.v1.api import api_router

logging.basicConfig(
    format="%(levelname)s %(pathname)s:%(funcName)s(%(lineno)d) %(message)s",
    level=logging.DEBUG if settings.ENV.is_development else logging.INFO,
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s in %s mode", settings.PROJECT_NAME, settings.ENV.value)
    yield
    logger.info("Shutting down %s", settings.PROJECT_NAME)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=settings.OPENAPI_URL,
        debug=settings.ENV.is_development,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).rstrip("/") for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=[
            "Accept",
            "Accept-Language",
            "Content-Language",
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "X-Request-ID",
        ],
        expose_headers=["X-Request-ID", "X-RateLimit-Remaining", "X-RateLimit-Limit"],
    )

    _configure_middlewares(app)
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/health", tags=["Health"])
    async def health_check() -> dict:
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "environment": settings.ENV.value,
        }

    return app


def _configure_middlewares(app: FastAPI) -> None:
    # Last added middleware runs first.
    app.add_middleware(RateLimitMiddleware)

    if settings.ENABLE_INPUT_VALIDATION:
        app.add_middleware(InputValidationMiddleware)

    if settings.ENABLE_REQUEST_LOGGING:
        app.add_middleware(RequestLoggingMiddleware)

    app.add_middleware(DBSessionMiddleware)

    if settings.ENABLE_SECURITY_HEADERS:
        app.add_middleware(SecurityHeadersMiddleware)

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Process-Time"] = f"{time.perf_counter() - start_time:.4f}"
        return response


app = create_app()
