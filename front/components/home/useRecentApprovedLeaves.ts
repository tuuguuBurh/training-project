import { useApi } from '~/composables/useApi'
import { API_ENDPOINTS } from '~/constants'
import type { LeaveRequestResponse, LeaveType } from '~/types/leave-request/leave-request-types'
import { mapApiToLeaveRequest } from '~/components/leave-requests/UseleaveRequests'
import type { LeaveRequest } from '~/components/leave-requests/LeaveRequest'
import { buildDatesBetween, dateRangeForPeriod, toDateKey } from './recent-approved-leaves-dates'
import type { RecentApprovedLeaveFilterState } from './recent-approved-leaves-types'

export const RECENT_APPROVED_DAYS = 7

export interface LeaveDayGroup {
  date: string
  label: string
  subtitle: string
  requests: LeaveRequest[]
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

function matchesSearch(request: LeaveRequest, search: string) {
  const query = search.trim().toLowerCase()
  if (!query) {
    return true
  }
  return request.employee.name.toLowerCase().includes(query) || request.employee.email.toLowerCase().includes(query)
}

function sortRequests(requests: LeaveRequest[], sort: RecentApprovedLeaveFilterState['sort']) {
  const sorted = [...requests]
  if (sort === 'name') {
    return sorted.sort((a, b) => a.employee.name.localeCompare(b.employee.name, 'mn'))
  }
  if (sort === 'oldest') {
    return sorted.sort((a, b) => a.submittedAt.localeCompare(b.submittedAt))
  }
  return sorted.sort((a, b) => b.submittedAt.localeCompare(a.submittedAt))
}

export function groupLeaveRequestsByDay(
  requests: LeaveRequest[],
  startDate: string,
  endDate: string,
): LeaveDayGroup[] {
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

  return buildDatesBetween(startDate, endDate).map((date) => ({
    date,
    label: formatDayLabel(date, todayKey),
    subtitle: formatDaySubtitle(date),
    requests: grouped.get(date) || [],
  }))
}

const defaultRange = dateRangeForPeriod('week')

export function useRecentApprovedLeaves() {
  const api = useApi()
  const leaveRequests = ref<LeaveRequest[]>([])
  const leaveTypes = ref<LeaveType[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const filters = ref<RecentApprovedLeaveFilterState>({
    period: 'week',
    startDate: defaultRange.startDate,
    endDate: defaultRange.endDate,
    search: '',
    leaveTypeId: 'all',
    sort: 'newest',
  })

  const dayGroups = computed(() => {
    const grouped = groupLeaveRequestsByDay(leaveRequests.value, filters.value.startDate, filters.value.endDate)
    return grouped
      .map((group) => {
        const filtered = group.requests.filter((request) => {
          if (filters.value.leaveTypeId !== 'all' && request.leaveType.id !== filters.value.leaveTypeId) {
            return false
          }
          return matchesSearch(request, filters.value.search)
        })
        return {
          ...group,
          requests: sortRequests(filtered, filters.value.sort),
        }
      })
      .filter((group) => group.requests.length > 0)
  })

  async function fetchLeaveTypes() {
    const { data } = await api.get<LeaveType[]>(API_ENDPOINTS.LEAVE_TYPES.LIST)
    leaveTypes.value = data || []
  }

  async function fetchRecentApprovedLeaves() {
    loading.value = true
    error.value = null

    const query = new URLSearchParams({
      from_date: filters.value.startDate,
      to_date: filters.value.endDate,
    })
    const path = `${API_ENDPOINTS.LEAVE_REQUESTS.RECENT_APPROVED}?${query.toString()}`
    const { data, error: apiError } = await api.get<LeaveRequestResponse[]>(path)

    loading.value = false

    if (apiError) {
      error.value = apiError.message
      leaveRequests.value = []
      return
    }

    leaveRequests.value = (data || []).map(mapApiToLeaveRequest)
  }

  watch(
    () => [filters.value.startDate, filters.value.endDate],
    () => {
      fetchRecentApprovedLeaves()
    },
  )

  return {
    leaveRequests,
    leaveTypes,
    dayGroups,
    filters,
    loading,
    error,
    fetchRecentApprovedLeaves,
    fetchLeaveTypes,
  }
}
