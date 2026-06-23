export interface LeaveType {
  id: string
  name: string
}

export interface TeamMember {
  id: string
  name: string
}

export interface LeaveRequestFormState {
  leaveTypeId: string
  startDate: string
  startTime: string
  endTime: string
  description: string
  approverIds: string[]
}

export interface LeaveRequestCreatePayload {
  leave_type_id: string
  start_date: string
  start_time: string
  end_time: string
  description?: string | null
  approver_ids: string[]
}

export interface LeaveRequestResponse {
  id: string
  requester: {
    id: string
    name: string
    email: string
  }
  leave_type: LeaveType
  start_date: string
  start_time: string
  end_time: string
  description: string | null
  status: string
  approvers: Array<{
    id: string
    approver_id: string
    approver_name: string
    decision: string
    decided_at: string | null
    rejection_reason: string | null
  }>
  created_at: string | null
  admin_name?: string | null
  admin_decision?: string | null
  admin_rejection_reason?: string | null
  admin_decided_at?: string | null
}
