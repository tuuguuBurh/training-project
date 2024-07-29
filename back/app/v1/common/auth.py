from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app.core.auth import authenticate_user, create_access_token
from app.v1 import deps

router = APIRouter()


@router.post("/login")
def login(
    request: Request,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    user = authenticate_user(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email or password is incorrect!")

    return {
        "access_token": create_access_token(sub=str(user.email)),
        "token_type": "bearer",
    }
