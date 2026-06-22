from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.auth import authenticate_user, create_access_token
from app.schemas.user import Token, UserResponse
from app.v1.deps import ActiveUser, DbSession

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    db: DbSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Authenticate user and return access token."""
    user = authenticate_user(db=db, email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return Token(access_token=create_access_token(sub=user.email))


@router.get("/me", response_model=UserResponse)
def get_current_user(user: ActiveUser) -> UserResponse:
    """Get current authenticated user profile."""
    return UserResponse.model_validate(user)
