from datetime import date, datetime, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class LeaveTypeResponse(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class TeamMemberResponse(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class LeaveRequestCreate(BaseModel):
    leave_type_id: UUID
    start_date: date
    start_time: time
    end_time: time
    description: str | None = Field(default=None, max_length=2000)
    approver_ids: list[UUID] = Field(default_factory=list, min_length=1)

    @field_validator("end_time")
    @classmethod
    def end_time_after_start(cls, end_time: time, info) -> time:
        start_time = info.data.get("start_time")
        if start_time and end_time <= start_time:
            raise ValueError("Дуусах цаг эхлэх цагаас хойш байх ёстой")
        return end_time


class RequesterResponse(BaseModel):
    id: UUID
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class LeaveRequestApproverResponse(BaseModel):
    id: UUID
    approver_id: UUID
    approver_name: str
    decision: str
    decided_at: datetime | None = None
    rejection_reason: str | None = None

    model_config = ConfigDict(from_attributes=True)


class LeaveRequestResponse(BaseModel):
    id: UUID
    requester: RequesterResponse
    leave_type: LeaveTypeResponse
    start_date: date
    start_time: time
    end_time: time
    description: str | None
    status: str
    approvers: list[LeaveRequestApproverResponse]
    created_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
