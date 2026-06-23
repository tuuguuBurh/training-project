import { useApi } from '~/composables/useApi'
import { API_ENDPOINTS } from '~/constants'
import type { LeaveRequestResponse } from '~/types/leave-request/leave-request-types'
import { mapApiToLeaveRequest, type LeaveListParams } from '~/components/leave-requests/UseleaveRequests'
import type { LeaveRequest } from '~/components/leave-requests/LeaveRequest'

export function useMyLeaveRequests() {
  const api = useApi()
  const leaveRequests = ref<LeaveRequest[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchMyLeaveRequests(params: LeaveListParams = {}) {
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
      ? `${API_ENDPOINTS.LEAVE_REQUESTS.MINE}?${query.toString()}`
      : API_ENDPOINTS.LEAVE_REQUESTS.MINE

    const { data, error: apiError } = await api.get<LeaveRequestResponse[]>(path)

    loading.value = false

    if (apiError) {
      error.value = apiError.message
      leaveRequests.value = []
      return
    }

    leaveRequests.value = (data || []).map(mapApiToLeaveRequest)
  }

  return { leaveRequests, loading, error, fetchMyLeaveRequests }
}
