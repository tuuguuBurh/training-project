from datetime import date as date_type
from uuid import UUID

from fastapi import APIRouter, Query

from app import crud
from app.models.leave_request import LeaveRequestStatus
from app.schemas.admin import (
    AdminEmployeeResponse,
    DashboardStatsResponse,
    LeaveReportItemResponse,
    LeaveTypeStatResponse,
    MonthlyTrendItemResponse,
)
from app.v1.deps import AdminUser, DbSession

router = APIRouter()


@router.get("/dashboard/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(_: AdminUser, db: DbSession) -> DashboardStatsResponse:
    return DashboardStatsResponse(**crud.admin.get_dashboard_stats(db=db))


@router.get("/dashboard/leave-types", response_model=list[LeaveTypeStatResponse])
def get_leave_type_stats(_: AdminUser, db: DbSession) -> list[LeaveTypeStatResponse]:
    return [LeaveTypeStatResponse(**item) for item in crud.admin.get_leave_type_stats(db=db)]


@router.get("/dashboard/monthly-trend", response_model=list[MonthlyTrendItemResponse])
def get_monthly_trend(
    _: AdminUser,
    db: DbSession,
    months: int = Query(default=12, ge=1, le=24),
) -> list[MonthlyTrendItemResponse]:
    return [MonthlyTrendItemResponse(**item) for item in crud.admin.get_monthly_trend(db=db, months=months)]


@router.get("/employees", response_model=list[AdminEmployeeResponse])
def list_employees(_: AdminUser, db: DbSession) -> list[AdminEmployeeResponse]:
    return [AdminEmployeeResponse.model_validate(item) for item in crud.admin.list_active_employees(db=db)]


@router.get("/reports/leaves", response_model=list[LeaveReportItemResponse])
def get_leave_report(
    _: AdminUser,
    db: DbSession,
    from_date: date_type | None = Query(default=None),
    to_date: date_type | None = Query(default=None),
    employee_id: UUID | None = Query(default=None),
    leave_type_id: UUID | None = Query(default=None),
    status: LeaveRequestStatus | None = Query(default=None),
) -> list[LeaveReportItemResponse]:
    items = crud.admin.list_report_requests(
        db=db,
        from_date=from_date,
        to_date=to_date,
        employee_id=employee_id,
        leave_type_id=leave_type_id,
        status=status,
    )

    return [
        LeaveReportItemResponse(
            id=item.id,
            employee_name=item.requester.name,
            leave_type=item.leave_type.name,
            start_date=item.start_date,
            end_date=item.start_date,
            total_days=crud.admin.compute_leave_days(start_time=item.start_time, end_time=item.end_time),
            status=item.status.value,
        )
        for item in items
    ]
