import type { Approver, LeaveRequest } from './LeaveRequest'

export function useLeaveRequestDetail(request: Ref<LeaveRequest | null>) {
  const { user } = useAuth()

  const isAdmin = computed(() => user.value?.role === 'ADMIN')

  const currentUserApprover = computed<Approver | null>(() => {
    if (!request.value || !user.value?.id) return null
    return request.value.approvers.find((approver) => approver.approverId === user.value?.id) ?? null
  })

  const isAssignedApprover = computed(() => !!currentUserApprover.value)

  const canViewDescription = computed(() => {
    if (!request.value) return false
    if (isAdmin.value) return true
    return isAssignedApprover.value
  })

  function isCurrentApprover(approver: Approver) {
    return !!user.value?.id && approver.approverId === user.value.id
  }

  return {
    user,
    isAdmin,
    currentUserApprover,
    isAssignedApprover,
    canViewDescription,
    isCurrentApprover,
  }
}
