from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def get_by_email(db: Session, *, email: str) -> User | None:
    stmt = select(User).where(User.email == email.strip().lower())
    return db.scalars(stmt).first()


def get_active_team_members(db: Session, *, exclude_user_id: UUID) -> list[User]:
    stmt = (
        select(User)
        .where(User.is_active.is_(True), User.id != exclude_user_id)
        .order_by(User.name)
    )
    return list(db.scalars(stmt).all())


def get_active_by_ids(db: Session, *, user_ids: list[UUID]) -> list[User]:
    if not user_ids:
        return []

    stmt = select(User).where(User.is_active.is_(True), User.id.in_(user_ids))
    return list(db.scalars(stmt).all())
