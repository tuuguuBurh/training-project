from datetime import date as date_type
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app import crud
from app.models.leave_request import ApproverDecisionStatus, LeaveRequest, LeaveRequestStatus
from app.models.user import User, UserRole
from app.schemas.leave_request import (
    AdminStatusUpdate,
    ApproverDecisionUpdate,
    LeaveRequestApproverResponse,
    LeaveRequestCreate,
    LeaveRequestResponse,
    LeaveTypeResponse,
    RequesterResponse,
    TeamMemberResponse,
)
from app.v1.deps import ActiveUser, DbSession

router = APIRouter()
leave_types_router = APIRouter()


def _can_view_description(leave_request: LeaveRequest, user: User) -> bool:
    if user.role == UserRole.ADMIN:
        return True
    if leave_request.user_id == user.id:
        return True
    return any(approver.approver_id == user.id for approver in leave_request.approvers)


def _to_response(leave_request: LeaveRequest, current_user: User | None = None) -> LeaveRequestResponse:
    description = leave_request.description
    if current_user and not _can_view_description(leave_request, current_user):
        description = None

    return LeaveRequestResponse(
        id=leave_request.id,
        requester=RequesterResponse.model_validate(leave_request.requester),
        leave_type=LeaveTypeResponse.model_validate(leave_request.leave_type),
        start_date=leave_request.start_date,
        start_time=leave_request.start_time,
        end_time=leave_request.end_time,
        description=description,
        status=leave_request.status.value,
        approvers=[
            LeaveRequestApproverResponse(
                id=approver.id,
                approver_id=approver.approver_id,
                approver_name=approver.approver.name,
                decision=approver.decision.value,
                decided_at=approver.decided_at,
                rejection_reason=approver.rejection_reason,
            )
            for approver in leave_request.approvers
        ],
        created_at=leave_request.created_at,
        admin_name=leave_request.admin.name if leave_request.admin else None,
        admin_decision=leave_request.admin_decision.value if leave_request.admin_decision else None,
        admin_rejection_reason=leave_request.admin_rejection_reason,
        admin_decided_at=leave_request.admin_decided_at,
    )


@leave_types_router.get("", response_model=list[LeaveTypeResponse])
def list_leave_types(db: DbSession, _: ActiveUser) -> list[LeaveTypeResponse]:
    return [LeaveTypeResponse.model_validate(item) for item in crud.leave_type.get_active(db=db)]


@router.get("", response_model=list[LeaveRequestResponse])
def list_leave_requests(
    db: DbSession,
    user: ActiveUser,
    on_date: date_type | None = Query(default=None, alias="date"),
    year: int | None = Query(default=None, ge=2000, le=2100),
    month: int | None = Query(default=None, ge=1, le=12),
) -> list[LeaveRequestResponse]:
    """Чөлөөний хүсэлтүүдийг өдөр эсвэл сараар шүүж буцаана. Default: өнөөдөр."""
    if year is not None and month is not None:
        items = crud.leave_request.list_requests(db=db, year=year, month=month)
    else:
        items = crud.leave_request.list_requests(db=db, on_date=on_date or date_type.today())
    return [_to_response(item, user) for item in items]


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
    return _to_response(leave_request, user)


@router.patch("/{leave_request_id}/my-decision", response_model=LeaveRequestResponse)
def update_my_approver_decision(
    leave_request_id: UUID,
    db: DbSession,
    user: ActiveUser,
    payload: ApproverDecisionUpdate,
) -> LeaveRequestResponse:
    decision = ApproverDecisionStatus(payload.decision)
    try:
        leave_request = crud.leave_request.decide_as_approver(
            db=db,
            leave_request_id=leave_request_id,
            approver_user_id=user.id,
            decision=decision,
            rejection_reason=payload.rejection_reason,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if not leave_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Хүсэлт олдсонгүй эсвэл та зөвшөөрөгч биш байна",
        )

    return _to_response(leave_request, user)


@router.patch("/{leave_request_id}/status", response_model=LeaveRequestResponse)
def update_leave_request_status(
    leave_request_id: UUID,
    db: DbSession,
    user: ActiveUser,
    payload: AdminStatusUpdate,
) -> LeaveRequestResponse:
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Зөвхөн админ ерөнхий төлөв өөрчлөх боломжтой",
        )

    new_status = LeaveRequestStatus(payload.status)
    try:
        leave_request = crud.leave_request.update_status_as_admin(
            db=db,
            leave_request_id=leave_request_id,
            admin_id=user.id,
            status=new_status,
            rejection_reason=payload.rejection_reason,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if not leave_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Хүсэлт олдсонгүй",
        )

    return _to_response(leave_request, user)
