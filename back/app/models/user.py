import enum
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.db.base_class import Base
from app.models.default import Default

if TYPE_CHECKING:
    from app.models.leave_request import LeaveRequest, LeaveRequestApprover


class UserRole(str, enum.Enum):
    USER = "USER"
    APPROVER = "APPROVER"
    ADMIN = "ADMIN"


class User(Base, Default):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, server_default=func.uuid_generate_v4()
    )
    email: Mapped[str] = mapped_column(String, index=True, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"), nullable=False, server_default=UserRole.USER.value
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="True")

    leave_requests: Mapped[list["LeaveRequest"]] = relationship(
        "LeaveRequest",
        back_populates="requester",
        foreign_keys="LeaveRequest.user_id",
    )
    leave_approvals: Mapped[list["LeaveRequestApprover"]] = relationship(
        "LeaveRequestApprover",
        back_populates="approver",
    )
    admin_decided_leave_requests: Mapped[list["LeaveRequest"]] = relationship(
        "LeaveRequest",
        back_populates="admin",
        foreign_keys="LeaveRequest.admin_id",
    )

    @validates("email")
    def convert_lower(self, key: str, value: str) -> str:
        return value.strip().lower()
