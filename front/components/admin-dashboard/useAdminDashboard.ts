import { useApi } from '~/composables/useApi'
import { API_ENDPOINTS } from '~/constants'
import type { DashboardStats, LeaveTypeStat, MonthlyTrendItem } from '~/types/admin/admin-types'

export function useAdminDashboard() {
  const api = useApi()
  const stats = ref<DashboardStats | null>(null)
  const leaveTypeStats = ref<LeaveTypeStat[]>([])
  const monthlyTrend = ref<MonthlyTrendItem[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchDashboard() {
    loading.value = true
    error.value = null

    const [statsResult, typesResult, trendResult] = await Promise.all([
      api.get<DashboardStats>(API_ENDPOINTS.ADMIN.DASHBOARD_STATS),
      api.get<LeaveTypeStat[]>(API_ENDPOINTS.ADMIN.LEAVE_TYPES),
      api.get<MonthlyTrendItem[]>(API_ENDPOINTS.ADMIN.MONTHLY_TREND),
    ])

    loading.value = false

    if (statsResult.error || typesResult.error || trendResult.error) {
      error.value = statsResult.error?.message || typesResult.error?.message || trendResult.error?.message || 'Алдаа'
      return
    }

    stats.value = statsResult.data
    leaveTypeStats.value = typesResult.data || []
    monthlyTrend.value = trendResult.data || []
  }

  return { stats, leaveTypeStats, monthlyTrend, loading, error, fetchDashboard }
}
