import logging

from sqlalchemy.orm import Session

from app import crud
from app.models.user import User, UserRole
from app.utils.functions import load_data

logger = logging.getLogger(__name__)


def create_users(db: Session) -> None:
    for row in load_data("users.json"):
        email = row["email"].strip().lower()
        if crud.user.get_by_email(db=db, email=email):
            logger.info("User with email `%s` already exists.", email)
            continue

        db.add(
            User(
                email=email,
                password=row["password"],
                name=row["name"],
                role=UserRole(row.get("role", UserRole.USER.value)),
                is_active=row.get("is_active", True),
            )
        )

    db.commit()
