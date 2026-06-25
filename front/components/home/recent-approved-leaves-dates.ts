import type { RecentApprovedLeavePeriod } from './recent-approved-leaves-types'

export function toDateKey(value: Date) {
  const year = value.getFullYear()
  const month = String(value.getMonth() + 1).padStart(2, '0')
  const day = String(value.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

export function todayDateKey() {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return toDateKey(today)
}

export function dateRangeForPeriod(period: RecentApprovedLeavePeriod) {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const endDate = toDateKey(today)

  if (period === 'today') {
    return { startDate: endDate, endDate }
  }

  if (period === 'week') {
    const start = new Date(today)
    start.setDate(today.getDate() - 6)
    return { startDate: toDateKey(start), endDate }
  }

  const monthStart = new Date(today.getFullYear(), today.getMonth(), 1)
  return { startDate: toDateKey(monthStart), endDate }
}

export function formatShortDate(dateKey: string) {
  const [, month, day] = dateKey.split('-')
  return `${month}/${day}`
}

export function formatDateRangeLabel(startDate: string, endDate: string) {
  return `${formatShortDate(startDate)} – ${formatShortDate(endDate)}`
}

export function buildDatesBetween(startDate: string, endDate: string) {
  const start = new Date(`${startDate}T00:00:00`)
  const end = new Date(`${endDate}T00:00:00`)
  const dates: string[] = []
  const current = new Date(end)

  while (current >= start) {
    dates.push(toDateKey(current))
    current.setDate(current.getDate() - 1)
  }

  return dates
}

export function normalizeDateRange(startDate: string, endDate: string) {
  if (startDate <= endDate) {
    return { startDate, endDate }
  }
  return { startDate: endDate, endDate: startDate }
}
