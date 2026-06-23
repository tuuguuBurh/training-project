import { useApi } from '~/composables/useApi'
import { API_ENDPOINTS } from '~/constants'
import type { LeaveRequestResponse } from '~/types/leave-request/leave-request-types'
import { mapApiToLeaveRequest } from './UseleaveRequests'
import type { LeaveRequest } from './LeaveRequest'

export function useLeaveRequestActions() {
  const api = useApi()
  const { $toast } = useNuxtApp()
  const submitting = ref(false)

  async function submitApproverDecision(
    requestId: string,
    decision: 'APPROVED' | 'REJECTED',
    rejectionReason?: string
  ): Promise<LeaveRequest | null> {
    submitting.value = true
    const { data, error } = await api.patch<LeaveRequestResponse>(
      API_ENDPOINTS.LEAVE_REQUESTS.MY_DECISION(requestId),
      {
        decision,
        rejection_reason: rejectionReason?.trim() || null,
      }
    )
    submitting.value = false

    if (error || !data) {
      $toast.error(error?.message || 'Шийдвэр хадгалахад алдаа гарлаа')
      return null
    }

    $toast.success(decision === 'APPROVED' ? 'Зөвшөөрсөн' : 'Татгалзсан')
    return mapApiToLeaveRequest(data)
  }

  async function submitAdminStatus(
    requestId: string,
    status: 'APPROVED' | 'REJECTED',
    rejectionReason?: string
  ): Promise<LeaveRequest | null> {
    submitting.value = true
    const { data, error } = await api.patch<LeaveRequestResponse>(API_ENDPOINTS.LEAVE_REQUESTS.STATUS(requestId), {
      status,
      rejection_reason: rejectionReason?.trim() || null,
    })
    submitting.value = false

    if (error || !data) {
      $toast.error(error?.message || 'Төлөв хадгалахад алдаа гарлаа')
      return null
    }

    $toast.success('Төлөв амжилттай шинэчлэгдлээ')
    return mapApiToLeaveRequest(data)
  }

  return {
    submitting: readonly(submitting),
    submitApproverDecision,
    submitAdminStatus,
  }
}
