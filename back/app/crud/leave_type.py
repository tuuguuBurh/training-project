from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.leave_type import LeaveType


def get_active(db: Session) -> list[LeaveType]:
    stmt = select(LeaveType).where(LeaveType.is_active.is_(True)).order_by(LeaveType.name)
    return list(db.scalars(stmt).all())


def get_by_id(db: Session, *, leave_type_id: UUID) -> LeaveType | None:
    stmt = select(LeaveType).where(
        LeaveType.id == leave_type_id,
        LeaveType.is_active.is_(True),
    )
    return db.scalars(stmt).first()
