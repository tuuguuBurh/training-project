from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jose import jwt
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.core.security import verify_password
from app.models.user import User


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = crud.user.get_by_email(db=db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(sub: str, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token.

    Args:
        sub: Subject (typically user email or ID)
        expires_delta: Optional custom expiration time
    """
    lifetime = expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_token(token_type="access_token", lifetime=lifetime, sub=sub)


def _create_token(token_type: str, lifetime: timedelta, sub: str) -> str:
    """Create a JWT token with the given parameters."""
    tz = ZoneInfo(settings.TIMEZONE)
    now = datetime.now(tz)

    payload = {
        "type": token_type,
        "exp": now + lifetime,
        "iat": now,
        "sub": sub,
    }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
