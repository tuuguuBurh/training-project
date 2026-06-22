from fastapi import APIRouter, HTTPException, status

from app import crud
from app.models.leave_request import LeaveRequest
from app.schemas.leave_request import (
    LeaveRequestApproverResponse,
    LeaveRequestCreate,
    LeaveRequestResponse,
    LeaveTypeResponse,
    TeamMemberResponse,
)
from app.v1.deps import ActiveUser, DbSession

router = APIRouter()
leave_types_router = APIRouter()


def _to_response(leave_request: LeaveRequest) -> LeaveRequestResponse:
    return LeaveRequestResponse(
        id=leave_request.id,
        leave_type=LeaveTypeResponse.model_validate(leave_request.leave_type),
        start_date=leave_request.start_date,
        start_time=leave_request.start_time,
        end_time=leave_request.end_time,
        description=leave_request.description,
        status=leave_request.status.value,
        approvers=[
            LeaveRequestApproverResponse(
                id=approver.id,
                approver_id=approver.approver_id,
                approver_name=approver.approver.name,
            )
            for approver in leave_request.approvers
        ],
        created_at=leave_request.created_at,
    )


@leave_types_router.get("", response_model=list[LeaveTypeResponse])
def list_leave_types(db: DbSession, _: ActiveUser) -> list[LeaveTypeResponse]:
    return [LeaveTypeResponse.model_validate(item) for item in crud.leave_type.get_active(db=db)]


@router.get("/team-members", response_model=list[TeamMemberResponse])
def list_team_members(db: DbSession, user: ActiveUser) -> list[TeamMemberResponse]:
    """Багийн гишүүд сонгоход ашиглах идэвхтэй хэрэглэгчид."""
    members = crud.user.get_active_team_members(db=db, exclude_user_id=user.id)
    return [TeamMemberResponse.model_validate(item) for item in members]


@router.post("", response_model=LeaveRequestResponse, status_code=status.HTTP_201_CREATED)
def create_leave_request(
    db: DbSession,
    user: ActiveUser,
    payload: LeaveRequestCreate,
) -> LeaveRequestResponse:
    leave_type = crud.leave_type.get_by_id(db=db, leave_type_id=payload.leave_type_id)
    if not leave_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Чөлөөний төрөл олдсонгүй",
        )

    if user.id in payload.approver_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Өөрийгөө багийн гишүүн болгон сонгох боломжгүй",
        )

    approvers = crud.user.get_active_by_ids(db=db, user_ids=payload.approver_ids)
    if len(approvers) != len(set(payload.approver_ids)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Багийн гишүүдийн зарим нь олдсонгүй эсвэл идэвхгүй байна",
        )

    leave_request = crud.leave_request.create(db=db, user_id=user.id, obj_in=payload)
    return _to_response(leave_request)
