import logging
import time
from collections import defaultdict, deque
from typing import Dict

from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings

logger = logging.getLogger(__name__)


class InMemoryRateLimiter:
    """
    Simple in-memory rate limiter using sliding window
    For production with multiple servers, consider using Redis
    """

    def __init__(self):
        self.requests: Dict[str, deque] = defaultdict(deque)

    def is_allowed(self, key: str, limit: int, window: int) -> bool:
        """
        Check if request is allowed based on rate limit

        Args:
            key: Identifier for the client (IP address + endpoint type)
            limit: Maximum number of requests allowed
            window: Time window in seconds

        Returns:
            True if request is allowed, False otherwise
        """
        now = time.time()

        # Clean old requests outside the window
        while self.requests[key] and self.requests[key][0] <= now - window:
            self.requests[key].popleft()

        # Check if limit is exceeded
        if len(self.requests[key]) >= limit:
            return False

        # Add current request timestamp
        self.requests[key].append(now)
        return True

    def get_remaining_requests(self, key: str, limit: int) -> int:
        """Get number of remaining requests for the key"""
        return max(0, limit - len(self.requests[key]))


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware for FastAPI
    Applies different rate limits based on endpoint patterns
    """

    def __init__(self, app):
        super().__init__(app)
        self.limiter = InMemoryRateLimiter()
        self.default_limit = settings.RATE_LIMIT_REQUESTS_PER_MINUTE
        self.auth_limit = settings.RATE_LIMIT_AUTH_REQUESTS_PER_MINUTE
        self.window = 60  # 1 minute window in seconds

    async def dispatch(self, request: Request, call_next):
        """Process request with rate limiting"""

        # Skip rate limiting for health checks and static files
        if self._should_skip_rate_limiting(request.url.path):
            return await call_next(request)

        client_ip = self._get_client_ip(request)

        # Determine rate limit based on endpoint
        if self._is_auth_endpoint(request.url.path):
            limit = self.auth_limit
            limit_type = "auth"
        else:
            limit = self.default_limit
            limit_type = "general"

        # Create unique key for this IP and endpoint type
        rate_limit_key = f"{client_ip}:{limit_type}"

        # Check rate limit
        if not self.limiter.is_allowed(rate_limit_key, limit, self.window):
            logger.warning(f"Rate limit exceeded for {client_ip} on {limit_type} endpoints")
            return Response(
                content=f"Rate limit exceeded. Maximum {limit} requests per minute allowed for {limit_type} endpoints.",
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                headers={
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Window": str(self.window),
                    "X-RateLimit-Reset": str(int(time.time()) + self.window),
                    "Retry-After": "60",
                },
            )

        # Continue with request processing
        response = await call_next(request)

        # Add rate limit headers to response
        remaining = self.limiter.get_remaining_requests(rate_limit_key, limit)
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Window"] = str(self.window)
        response.headers["X-RateLimit-Reset"] = str(int(time.time()) + self.window)

        return response

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address from request"""
        # Check for forwarded headers first (for reverse proxy scenarios)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # Take the first IP if multiple are present
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fall back to direct client IP
        return request.client.host if request.client else "unknown"

    def _is_auth_endpoint(self, path: str) -> bool:
        """Check if the endpoint is authentication related"""
        auth_patterns = [
            "/auth/login",
            "/auth/register",
            "/auth/refresh",
            "/auth/reset-password",
            "/auth/forgot-password",
            "/auth/token",
        ]
        return any(pattern in path for pattern in auth_patterns)

    def _should_skip_rate_limiting(self, path: str) -> bool:
        """Check if rate limiting should be skipped for this path"""
        skip_patterns = ["/health", "/docs", "/openapi.json", "/favicon.ico", "/static/"]
        return any(pattern in path for pattern in skip_patterns)
