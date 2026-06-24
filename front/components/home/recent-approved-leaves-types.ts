export type RecentApprovedLeavePeriod = 'today' | 'week' | 'month'
export type RecentApprovedLeaveSort = 'newest' | 'oldest' | 'name'

export interface RecentApprovedLeaveFilterState {
  period: RecentApprovedLeavePeriod | 'custom'
  startDate: string
  endDate: string
  search: string
  leaveTypeId: string | 'all'
  sort: RecentApprovedLeaveSort
}

export const RECENT_APPROVED_VISIBLE_COUNT = 5

export const PERIOD_CHIP_LABELS: Record<RecentApprovedLeavePeriod, string> = {
  today: 'Өнөөдөр',
  week: '7 хоног',
  month: 'Энэ сар',
}
