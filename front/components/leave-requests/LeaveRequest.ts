export type LeaveStatus = 'pending' | 'approved' | 'rejected'

export interface Approver {
  id: string
  approverId: string
  name: string
  status: LeaveStatus
  respondedAt?: string
  rejectionReason?: string
}

export interface Employee {
  id: string
  name: string
  email: string
}

export interface LeaveTypeInfo {
  id: string
  name: string
}

export interface AdminDecision {
  name?: string
  status: LeaveStatus
  rejectionReason?: string
  decidedAt?: string
}

export interface LeaveRequest {
  id: string
  employee: Employee
  leaveType: LeaveTypeInfo
  status: LeaveStatus
  startDate: string
  startTime: string
  endTime: string
  submittedAt: string
  approvers: Approver[]
  description?: string
  adminDecision?: AdminDecision
}

export const LEAVE_STATUS_LABELS: Record<LeaveStatus, string> = {
  pending: 'Хүлээгдэж буй',
  approved: 'Зөвшөөрсөн',
  rejected: 'Татгалзсан',
}

export function mapApiStatus(status: string): LeaveStatus {
  const normalized = status.toLowerCase() as LeaveStatus
  return normalized in LEAVE_STATUS_LABELS ? normalized : 'pending'
}
