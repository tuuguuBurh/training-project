import { useApi } from '~/composables/useApi'
import { API_ENDPOINTS } from '~/constants'
import type { LeaveRequestResponse } from '~/types/leave-request/leave-request-types'
import { mapApiToLeaveRequest } from '~/components/leave-requests/UseleaveRequests'
import type { LeaveRequest } from '~/components/leave-requests/LeaveRequest'

export const RECENT_APPROVED_DAYS = 7

export interface LeaveDayGroup {
  date: string
  label: string
  subtitle: string
  requests: LeaveRequest[]
}

function toDateKey(value: Date) {
  const year = value.getFullYear()
  const month = String(value.getMonth() + 1).padStart(2, '0')
  const day = String(value.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

function buildRecentDates(days: number) {
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  return Array.from({ length: days }, (_, index) => {
    const date = new Date(today)
    date.setDate(today.getDate() - index)
    return toDateKey(date)
  })
}

function formatDayLabel(dateKey: string, todayKey: string) {
  if (dateKey === todayKey) {
    return 'Өнөөдөр'
  }

  const target = new Date(`${dateKey}T00:00:00`)
  const today = new Date(`${todayKey}T00:00:00`)
  const diffDays = Math.round((today.getTime() - target.getTime()) / 86_400_000)

  if (diffDays === 1) {
    return 'Өчигдөр'
  }

  return new Intl.DateTimeFormat('mn-MN', {
    month: 'long',
    day: 'numeric',
  }).format(target)
}

function formatDaySubtitle(dateKey: string) {
  return new Intl.DateTimeFormat('mn-MN', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date(`${dateKey}T00:00:00`))
}

export function groupLeaveRequestsByDay(requests: LeaveRequest[], days = RECENT_APPROVED_DAYS): LeaveDayGroup[] {
  const todayKey = toDateKey(new Date())
  const grouped = new Map<string, LeaveRequest[]>()

  for (const request of requests) {
    const existing = grouped.get(request.startDate)
    if (existing) {
      existing.push(request)
      continue
    }
    grouped.set(request.startDate, [request])
  }

  return buildRecentDates(days).map((date) => ({
    date,
    label: formatDayLabel(date, todayKey),
    subtitle: formatDaySubtitle(date),
    requests: grouped.get(date) || [],
  }))
}

export function useRecentApprovedLeaves() {
  const api = useApi()
  const leaveRequests = ref<LeaveRequest[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchRecentApprovedLeaves(days = RECENT_APPROVED_DAYS) {
    loading.value = true
    error.value = null

    const path = `${API_ENDPOINTS.LEAVE_REQUESTS.RECENT_APPROVED}?days=${days}`
    const { data, error: apiError } = await api.get<LeaveRequestResponse[]>(path)

    loading.value = false

    if (apiError) {
      error.value = apiError.message
      leaveRequests.value = []
      return
    }

    leaveRequests.value = (data || []).map(mapApiToLeaveRequest)
  }

  const dayGroups = computed(() => groupLeaveRequestsByDay(leaveRequests.value))

  return {
    leaveRequests,
    dayGroups,
    loading,
    error,
    fetchRecentApprovedLeaves,
  }
}
