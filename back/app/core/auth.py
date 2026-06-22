from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jose import jwt
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.models.user import User


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Authenticate user with plain-text password (NO HASH)."""

    normalized_email = email.strip().lower()
    user = crud.user.get_by_email(db=db, email=normalized_email)

    if not user:
        return None

    # clean compare (avoid hidden spaces)
    if user.password.strip() != password.strip():
        return None

    return user


def create_access_token(sub: str, expires_delta: timedelta | None = None) -> str:
    """Create JWT token."""

    lifetime = expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return _create_token(
        token_type="access_token",
        lifetime=lifetime,
        sub=sub,
    )


def _create_token(*, token_type: str, lifetime: timedelta, sub: str) -> str:
    tz = ZoneInfo(settings.TIMEZONE)
    now = datetime.now(tz)

    payload = {
        "type": token_type,
        "sub": sub,
        "iat": int(now.timestamp()),
        "exp": int((now + lifetime).timestamp()),
    }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
