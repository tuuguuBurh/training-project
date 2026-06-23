import { useApi } from '~/composables/useApi'
import { API_ENDPOINTS } from '~/constants'
import type { AdminEmployee, LeaveReportFilters, LeaveReportItem } from '~/types/admin/admin-types'
import type { LeaveType } from '~/types/leave-request/leave-request-types'

function defaultFilters(): LeaveReportFilters {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const lastDay = new Date(year, now.getMonth() + 1, 0).getDate()
  return {
    fromDate: `${year}-${month}-01`,
    toDate: `${year}-${month}-${String(lastDay).padStart(2, '0')}`,
    employeeId: 'all',
    leaveTypeId: 'all',
    status: 'all',
  }
}

export function useAdminLeaveReport() {
  const api = useApi()
  const filters = ref<LeaveReportFilters>(defaultFilters())
  const reportItems = ref<LeaveReportItem[]>([])
  const employees = ref<AdminEmployee[]>([])
  const leaveTypes = ref<LeaveType[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const hasGenerated = ref(false)

  async function fetchFilterOptions() {
    const [employeesResult, typesResult] = await Promise.all([
      api.get<AdminEmployee[]>(API_ENDPOINTS.ADMIN.EMPLOYEES),
      api.get<LeaveType[]>(API_ENDPOINTS.LEAVE_TYPES.LIST),
    ])

    employees.value = employeesResult.data || []
    leaveTypes.value = typesResult.data || []
  }

  async function generateReport() {
    loading.value = true
    error.value = null

    const query = new URLSearchParams()
    if (filters.value.fromDate) query.set('from_date', filters.value.fromDate)
    if (filters.value.toDate) query.set('to_date', filters.value.toDate)
    if (filters.value.employeeId !== 'all') query.set('employee_id', filters.value.employeeId)
    if (filters.value.leaveTypeId !== 'all') query.set('leave_type_id', filters.value.leaveTypeId)
    if (filters.value.status !== 'all') query.set('status', filters.value.status.toUpperCase())

    const path = `${API_ENDPOINTS.ADMIN.LEAVE_REPORT}?${query.toString()}`
    const { data, error: apiError } = await api.get<LeaveReportItem[]>(path)

    loading.value = false
    hasGenerated.value = true

    if (apiError) {
      error.value = apiError.message
      reportItems.value = []
      return
    }

    reportItems.value = data || []
  }

  return {
    filters,
    reportItems,
    employees,
    leaveTypes,
    loading,
    error,
    hasGenerated,
    fetchFilterOptions,
    generateReport,
  }
}
