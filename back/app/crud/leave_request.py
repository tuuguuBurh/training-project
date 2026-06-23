import calendar
from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.leave_request import LeaveRequest, LeaveRequestApprover
from app.schemas.leave_request import LeaveRequestCreate

_LIST_OPTIONS = (
    selectinload(LeaveRequest.leave_type),
    selectinload(LeaveRequest.requester),
    selectinload(LeaveRequest.approvers).selectinload(LeaveRequestApprover.approver),
)


def create(
    db: Session,
    *,
    user_id: UUID,
    obj_in: LeaveRequestCreate,
) -> LeaveRequest:
    leave_request = LeaveRequest(
        user_id=user_id,
        leave_type_id=obj_in.leave_type_id,
        start_date=obj_in.start_date,
        start_time=obj_in.start_time,
        end_time=obj_in.end_time,
        description=obj_in.description,
    )
    db.add(leave_request)
    db.flush()

    for approver_id in obj_in.approver_ids:
        db.add(
            LeaveRequestApprover(
                leave_request_id=leave_request.id,
                approver_id=approver_id,
            )
        )

    db.commit()

    stmt = select(LeaveRequest).options(*_LIST_OPTIONS).where(LeaveRequest.id == leave_request.id)
    return db.scalars(stmt).one()


def list_requests(
    db: Session,
    *,
    on_date: date | None = None,
    year: int | None = None,
    month: int | None = None,
) -> list[LeaveRequest]:
    stmt = (
        select(LeaveRequest)
        .options(*_LIST_OPTIONS)
        .order_by(
            LeaveRequest.start_date.desc(),
            LeaveRequest.created_at.desc(),
        )
    )

    if year is not None and month is not None:
        start = date(year, month, 1)
        last_day = calendar.monthrange(year, month)[1]
        end = date(year, month, last_day)
        stmt = stmt.where(LeaveRequest.start_date >= start, LeaveRequest.start_date <= end)
    elif on_date is not None:
        stmt = stmt.where(LeaveRequest.start_date == on_date)

    return list(db.scalars(stmt).all())
