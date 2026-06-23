import { useApi } from '~/composables/useApi'
import { API_ENDPOINTS } from '~/constants'
import type { LeaveRequestResponse } from '~/types/leave-request/leave-request-types'
import { mapApiStatus, type LeaveRequest } from './LeaveRequest'

export interface LeaveListParams {
  date?: string
  year?: number
  month?: number
}

export function mapApiToLeaveRequest(item: LeaveRequestResponse): LeaveRequest {
  return {
    id: item.id,
    employee: {
      id: item.requester.id,
      name: item.requester.name,
      email: item.requester.email,
    },
    leaveType: {
      id: item.leave_type.id,
      name: item.leave_type.name,
    },
    status: mapApiStatus(item.status),
    startDate: item.start_date,
    startTime: item.start_time.slice(0, 5),
    endTime: item.end_time.slice(0, 5),
    submittedAt: item.created_at || new Date().toISOString(),
    approvers: item.approvers.map((approver) => ({
      id: approver.id,
      approverId: approver.approver_id,
      name: approver.approver_name,
      status: mapApiStatus(approver.decision),
      respondedAt: approver.decided_at || undefined,
      rejectionReason: approver.rejection_reason || undefined,
    })),
    description: item.description || undefined,
    adminDecision: item.admin_decision
      ? {
          name: item.admin_name || undefined,
          status: mapApiStatus(item.admin_decision),
          rejectionReason: item.admin_rejection_reason || undefined,
          decidedAt: item.admin_decided_at || undefined,
        }
      : undefined,
  }
}

export function useLeaveRequests() {
  const api = useApi()
  const leaveRequests = ref<LeaveRequest[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchLeaveRequests(params: LeaveListParams) {
    loading.value = true
    error.value = null

    const query = new URLSearchParams()
    if (params.year !== undefined && params.month !== undefined) {
      query.set('year', String(params.year))
      query.set('month', String(params.month))
    } else if (params.date) {
      query.set('date', params.date)
    }

    const path = query.toString()
      ? `${API_ENDPOINTS.LEAVE_REQUESTS.LIST}?${query.toString()}`
      : API_ENDPOINTS.LEAVE_REQUESTS.LIST

    const { data, error: apiError } = await api.get<LeaveRequestResponse[]>(path)

    loading.value = false

    if (apiError) {
      error.value = apiError.message
      leaveRequests.value = []
      return
    }

    leaveRequests.value = (data || []).map(mapApiToLeaveRequest)
  }

  return { leaveRequests, loading, error, fetchLeaveRequests }
}
