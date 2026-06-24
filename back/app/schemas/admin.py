from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DashboardStatsResponse(BaseModel):
    total_users: int
    total_requests: int
    pending_requests: int
    approved_requests: int
    rejected_requests: int
    total_leave_days: float


class LeaveTypeStatResponse(BaseModel):
    leave_type_id: UUID
    name: str
    count: int


class MonthlyTrendItemResponse(BaseModel):
    year: int
    month: int
    label: str
    count: int


class LeaveReportItemResponse(BaseModel):
    id: UUID
    employee_name: str
    leave_type: str
    start_date: date
    end_date: date
    total_days: float
    status: str


class AdminEmployeeResponse(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)
