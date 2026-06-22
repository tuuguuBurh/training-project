import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.leave_type import LeaveType
from app.utils.functions import load_data

logger = logging.getLogger(__name__)


def create_leave_types(db: Session) -> None:
    for row in load_data("leave_types.json"):
        name = row["name"]
        exists = db.scalars(select(LeaveType).where(LeaveType.name == name)).first()
        if exists:
            logger.info("Leave type `%s` already exists.", name)
            continue

        db.add(LeaveType(name=name, is_active=True))

    db.commit()
