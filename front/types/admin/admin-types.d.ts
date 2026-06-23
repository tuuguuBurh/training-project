export interface DashboardStats {
  total_users: number
  total_requests: number
  pending_requests: number
  approved_requests: number
  rejected_requests: number
  total_leave_days: number
}

export interface LeaveTypeStat {
  leave_type_id: string
  name: string
  count: number
}

export interface MonthlyTrendItem {
  year: number
  month: number
  label: string
  count: number
}

export interface LeaveReportItem {
  id: string
  employee_name: string
  leave_type: string
  start_date: string
  end_date: string
  total_days: number
  status: string
}

export interface AdminEmployee {
  id: string
  name: string
}

export interface LeaveReportFilters {
  fromDate: string
  toDate: string
  employeeId: string | 'all'
  leaveTypeId: string | 'all'
  status: string | 'all'
}
