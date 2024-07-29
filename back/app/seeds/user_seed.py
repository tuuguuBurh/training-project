import logging

from sqlalchemy.orm import Session

from app import crud, schemas
from app.utils.functions import load_data

logger = logging.getLogger(__name__)


def create_users(db: Session):
    for row in load_data("users.json"):
        email = row.get("email")
        if crud.user.get_by_email(db=db, email=email):
            logger.info(f"--User with `{email} has already exists.")
            continue

        obj_in = schemas.UserCreate(
            email=email,
            password=row.get("password"),
            is_active=True,
            first_name=row.get("first_name"),
            last_name=row.get("last_name"),
        )
        crud.user.create(db=db, obj_in=obj_in)
