import enum
import uuid
from datetime import date, datetime, time

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Text, Time, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.default import Default


class LeaveRequestStatus(str, enum.Enum):
    """Хүсэлтийн ерөнхий төлөв — admin эцсийн шийдвэр хүртэл PENDING."""

    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ApproverDecisionStatus(str, enum.Enum):
    """Багийн гишүүний зөвшөөрөл."""

    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class LeaveRequest(Base, Default):
    """Хэрэглэгчийн чөлөөний хүсэлт."""

    __tablename__ = "leave_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, server_default=func.uuid_generate_v4()
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    leave_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("leave_types.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[LeaveRequestStatus] = mapped_column(
        Enum(LeaveRequestStatus, name="leave_request_status"),
        nullable=False,
        server_default=LeaveRequestStatus.PENDING.value,
    )
    admin_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    admin_decision: Mapped[ApproverDecisionStatus | None] = mapped_column(
        Enum(ApproverDecisionStatus, name="admin_decision_status"), nullable=True
    )
    admin_rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    admin_decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    requester: Mapped["User"] = relationship(
        "User", back_populates="leave_requests", foreign_keys=[user_id]
    )
    admin: Mapped["User | None"] = relationship(
        "User", back_populates="admin_decided_leave_requests", foreign_keys=[admin_id]
    )
    leave_type: Mapped["LeaveType"] = relationship("LeaveType", back_populates="leave_requests")
    approvers: Mapped[list["LeaveRequestApprover"]] = relationship(
        "LeaveRequestApprover",
        back_populates="leave_request",
        cascade="all, delete-orphan",
    )


class LeaveRequestApprover(Base, Default):
    __tablename__ = "leave_request_approvers"
    __table_args__ = (UniqueConstraint("leave_request_id", "approver_id", name="uq_leave_request_approver"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, server_default=func.uuid_generate_v4()
    )
    leave_request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("leave_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    approver_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    decision: Mapped[ApproverDecisionStatus] = mapped_column(
        Enum(ApproverDecisionStatus, name="approver_decision_status"),
        nullable=False,
        server_default=ApproverDecisionStatus.PENDING.value,
    )
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    leave_request: Mapped["LeaveRequest"] = relationship("LeaveRequest", back_populates="approvers")
    approver: Mapped["User"] = relationship("User", back_populates="leave_approvals")
