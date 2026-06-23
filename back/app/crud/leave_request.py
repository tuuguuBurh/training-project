import calendar
from datetime import date, datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.leave_request import (
    ApproverDecisionStatus,
    LeaveRequest,
    LeaveRequestApprover,
    LeaveRequestStatus,
)
from app.schemas.leave_request import LeaveRequestCreate

_LIST_OPTIONS = (
    selectinload(LeaveRequest.leave_type),
    selectinload(LeaveRequest.requester),
    selectinload(LeaveRequest.admin),
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
    from_date: date | None = None,
    to_date: date | None = None,
    status: LeaveRequestStatus | None = None,
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
    elif from_date is not None and to_date is not None:
        stmt = stmt.where(LeaveRequest.start_date >= from_date, LeaveRequest.start_date <= to_date)
    elif on_date is not None:
        stmt = stmt.where(LeaveRequest.start_date == on_date)

    if status is not None:
        stmt = stmt.where(LeaveRequest.status == status)

    return list(db.scalars(stmt).all())


def get_by_id(db: Session, *, leave_request_id: UUID) -> LeaveRequest | None:
    stmt = select(LeaveRequest).options(*_LIST_OPTIONS).where(LeaveRequest.id == leave_request_id)
    return db.scalars(stmt).first()


def decide_as_approver(
    db: Session,
    *,
    leave_request_id: UUID,
    approver_user_id: UUID,
    decision: ApproverDecisionStatus,
    rejection_reason: str | None = None,
) -> LeaveRequest | None:
    leave_request = get_by_id(db=db, leave_request_id=leave_request_id)
    if not leave_request:
        return None

    approver_row = next(
        (row for row in leave_request.approvers if row.approver_id == approver_user_id),
        None,
    )
    if not approver_row:
        return None

    if decision == ApproverDecisionStatus.REJECTED and not (rejection_reason and rejection_reason.strip()):
        raise ValueError("Татгалзах үед тайлбар заавал оруулна")

    approver_row.decision = decision
    approver_row.rejection_reason = rejection_reason.strip() if decision == ApproverDecisionStatus.REJECTED else None
    approver_row.decided_at = datetime.now(timezone.utc)

    db.commit()
    return get_by_id(db=db, leave_request_id=leave_request_id)


def update_status_as_admin(
    db: Session,
    *,
    leave_request_id: UUID,
    admin_id: UUID,
    status: LeaveRequestStatus,
    rejection_reason: str | None = None,
) -> LeaveRequest | None:
    leave_request = get_by_id(db=db, leave_request_id=leave_request_id)
    if not leave_request:
        return None

    if status == LeaveRequestStatus.REJECTED and not (rejection_reason and rejection_reason.strip()):
        raise ValueError("Татгалзах үед тайлбар заавал оруулна")

    admin_decision = ApproverDecisionStatus(status.value)
    leave_request.status = status
    leave_request.admin_id = admin_id
    leave_request.admin_decision = admin_decision
    leave_request.admin_rejection_reason = rejection_reason.strip() if status == LeaveRequestStatus.REJECTED else None
    leave_request.admin_decided_at = datetime.now(timezone.utc)

    db.commit()
    return get_by_id(db=db, leave_request_id=leave_request_id)


def list_requests_by_user(
    db: Session,
    *,
    user_id: UUID,
    on_date: date | None = None,
    year: int | None = None,
    month: int | None = None,
) -> list[LeaveRequest]:
    stmt = (
        select(LeaveRequest)
        .options(*_LIST_OPTIONS)
        .where(LeaveRequest.user_id == user_id)
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
