from datetime import date, time
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.leave_request import LeaveRequest, LeaveRequestStatus
from app.models.leave_type import LeaveType
from app.models.user import User

_LIST_OPTIONS = (
    selectinload(LeaveRequest.leave_type),
    selectinload(LeaveRequest.requester),
)

_MONTH_LABELS = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)


def compute_leave_days(*, start_time: time, end_time: time) -> float:
    start_seconds = start_time.hour * 3600 + start_time.minute * 60 + start_time.second
    end_seconds = end_time.hour * 3600 + end_time.minute * 60 + end_time.second
    hours = max(0.0, (end_seconds - start_seconds) / 3600)
    if hours <= 0:
        return 1.0
    return round(hours / 8, 2)


def get_dashboard_stats(db: Session) -> dict[str, int | float]:
    total_users = db.scalar(select(func.count()).select_from(User).where(User.is_active.is_(True))) or 0
    total_requests = db.scalar(select(func.count()).select_from(LeaveRequest)) or 0
    pending_requests = (
        db.scalar(
            select(func.count()).select_from(LeaveRequest).where(LeaveRequest.status == LeaveRequestStatus.PENDING)
        )
        or 0
    )
    approved_requests = (
        db.scalar(
            select(func.count()).select_from(LeaveRequest).where(LeaveRequest.status == LeaveRequestStatus.APPROVED)
        )
        or 0
    )
    rejected_requests = (
        db.scalar(
            select(func.count()).select_from(LeaveRequest).where(LeaveRequest.status == LeaveRequestStatus.REJECTED)
        )
        or 0
    )

    approved_rows = db.execute(
        select(LeaveRequest.start_time, LeaveRequest.end_time).where(LeaveRequest.status == LeaveRequestStatus.APPROVED)
    ).all()
    total_leave_days = round(
        sum(compute_leave_days(start_time=row.start_time, end_time=row.end_time) for row in approved_rows),
        2,
    )

    return {
        "total_users": total_users,
        "total_requests": total_requests,
        "pending_requests": pending_requests,
        "approved_requests": approved_requests,
        "rejected_requests": rejected_requests,
        "total_leave_days": total_leave_days,
    }


def get_leave_type_stats(db: Session) -> list[dict[str, UUID | str | int]]:
    rows = db.execute(
        select(
            LeaveType.id,
            LeaveType.name,
            func.count(LeaveRequest.id).label("count"),
        )
        .outerjoin(LeaveRequest, LeaveRequest.leave_type_id == LeaveType.id)
        .where(LeaveType.is_active.is_(True))
        .group_by(LeaveType.id, LeaveType.name)
        .order_by(LeaveType.name)
    ).all()

    return [
        {
            "leave_type_id": row.id,
            "name": row.name,
            "count": row.count,
        }
        for row in rows
    ]


def get_monthly_trend(db: Session, *, months: int = 12) -> list[dict[str, int | str]]:
    today = date.today()
    month_starts: list[date] = []
    cursor = date(today.year, today.month, 1)
    for _ in range(months):
        month_starts.append(cursor)
        if cursor.month == 1:
            cursor = date(cursor.year - 1, 12, 1)
        else:
            cursor = date(cursor.year, cursor.month - 1, 1)
    month_starts.reverse()

    results: list[dict[str, int | str]] = []
    for month_start in month_starts:
        if month_start.month == 12:
            next_month = date(month_start.year + 1, 1, 1)
        else:
            next_month = date(month_start.year, month_start.month + 1, 1)

        count = (
            db.scalar(
                select(func.count())
                .select_from(LeaveRequest)
                .where(
                    LeaveRequest.created_at >= month_start,
                    LeaveRequest.created_at < next_month,
                )
            )
            or 0
        )
        results.append(
            {
                "year": month_start.year,
                "month": month_start.month,
                "label": _MONTH_LABELS[month_start.month - 1],
                "count": count,
            }
        )

    return results


def list_report_requests(
    db: Session,
    *,
    from_date: date | None = None,
    to_date: date | None = None,
    employee_id: UUID | None = None,
    leave_type_id: UUID | None = None,
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

    if from_date is not None:
        stmt = stmt.where(LeaveRequest.start_date >= from_date)
    if to_date is not None:
        stmt = stmt.where(LeaveRequest.start_date <= to_date)
    if employee_id is not None:
        stmt = stmt.where(LeaveRequest.user_id == employee_id)
    if leave_type_id is not None:
        stmt = stmt.where(LeaveRequest.leave_type_id == leave_type_id)
    if status is not None:
        stmt = stmt.where(LeaveRequest.status == status)

    return list(db.scalars(stmt).all())


def list_active_employees(db: Session) -> list[User]:
    stmt = select(User).where(User.is_active.is_(True)).order_by(User.name)
    return list(db.scalars(stmt).all())
