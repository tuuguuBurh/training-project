from datetime import datetime, timedelta
from typing import List, MutableMapping, Union

import pytz
from jose import jwt
from sqlalchemy.orm.session import Session

from app import crud
from app.core.config import settings
from app.core.security import verify_password
from app.models.user import User

JWTPayloadMapping = MutableMapping[str, Union[datetime, bool, str, List[str], List[int]]]


def authenticate_user(*, email: str, password: str, db: Session) -> User | None:
    user = crud.user.get_by_email(db=db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None

    return user


def create_access_token(*, sub: str) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(token_type: str, lifetime: timedelta, sub: str) -> str:
    payload = {}
    expire = datetime.now(pytz.timezone("Asia/Ulaanbaatar")) + lifetime
    payload["type"] = token_type

    payload["exp"] = expire
    payload["iat"] = datetime.now(pytz.timezone("Asia/Ulaanbaatar"))
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
