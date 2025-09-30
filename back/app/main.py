import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import AppENV, settings
from app.middlewares.db_session import DBSessionMiddleware
from app.middlewares.input_validation import InputValidationMiddleware
from app.middlewares.rate_limit import RateLimitMiddleware
from app.middlewares.request_logging import RequestLoggingMiddleware
from app.middlewares.security_headers import SecurityHeadersMiddleware
from app.v1.api_user import user_router

log_fmt = "%(pathname)s:%(funcName)s(%(lineno)d) %(message)s"
logging.basicConfig(
    format="%(levelname)s " + log_fmt,
    level=logging.DEBUG if settings.ENV == AppENV.LOCAL else logging.INFO,
)


def get_application():
    _debug = settings.ENV == AppENV.LOCAL
    _app = FastAPI(
        debug=_debug,
        title=settings.PROJECT_NAME,
        openapi_url=settings.OPENAPI_URL,
    )
    # Configure CORS with more restrictive settings
    allowed_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    allowed_headers = [
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "X-Request-ID",
    ]

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=allowed_methods,
        allow_headers=allowed_headers,
        expose_headers=["X-Request-ID", "X-RateLimit-Remaining", "X-RateLimit-Limit"],
    )
    return _app


app = get_application()

# Add middlewares in correct order (last added = first executed)
# Security headers should be last (first to execute)
app.add_middleware(SecurityHeadersMiddleware)

# Database session middleware
app.add_middleware(DBSessionMiddleware)

# Request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Input validation middleware
app.add_middleware(InputValidationMiddleware)

# Rate limiting middleware (should be early in the chain)
app.add_middleware(RateLimitMiddleware)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(user_router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health_check():
    """Health check endpoint (not rate limited)"""
    return {"status": "healthy", "timestamp": time.time()}


@app.get("/test-rate-limit")
async def test_rate_limit():
    """Test endpoint to verify rate limiting is working"""
    return {"message": "Rate limiting is working!", "timestamp": time.time()}
