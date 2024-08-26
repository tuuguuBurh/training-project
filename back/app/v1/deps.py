from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm.session import Session

from app import crud
from app.core.config import settings
from app.models.user import User

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class TokenData(BaseModel):
    email: Optional[str] = None


def get_db(request: Request):
    return request.state.db


user_oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login", scheme_name="User")


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(user_oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        sub: str = payload.get("sub")
        if not sub:
            raise credentials_exception

        token_data = TokenData(email=sub)
    except JWTError:
        raise credentials_exception

    user = crud.user.get_by_email(db=db, email=token_data.email)

    if user is None:
        raise credentials_exception

    return user
