from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.leave_request import LeaveRequest, LeaveRequestApprover
from app.schemas.leave_request import LeaveRequestCreate


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

    stmt = (
        select(LeaveRequest)
        .options(
            selectinload(LeaveRequest.leave_type),
            selectinload(LeaveRequest.approvers).selectinload(LeaveRequestApprover.approver),
        )
        .where(LeaveRequest.id == leave_request.id)
    )
    return db.scalars(stmt).one()
