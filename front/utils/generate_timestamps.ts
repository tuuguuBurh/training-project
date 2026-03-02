import { format, addMinutes, addHours, addDays, addWeeks, addMonths, parse } from 'date-fns'
import type { AggregatorType } from '~/types/GraphDataType'

export function generateTimestamps(start_time: string, end_time: string, aggregator: AggregatorType) {
  const startDate = new Date(start_time)
  const endDate = new Date(end_time)
  const timestamps = []
  let currentDate = startDate
  const formatString = aggregator === 'minute' || aggregator === 'hour' ? 'yyyy/MM/dd HH:mm' : 'yyyy/MM/dd'

  while (currentDate <= endDate) {
    timestamps.push(format(currentDate, formatString))
    switch (aggregator) {
      case 'minute':
        currentDate = addMinutes(currentDate, 1)
        break
      case 'hour':
        currentDate = addHours(currentDate, 1)
        break
      case 'day':
        currentDate = addDays(currentDate, 1)
        break
      case 'month':
        currentDate = addMonths(currentDate, 1)
        break
      default:
        throw new Error('Invalid aggregator')
    }
  }

  return timestamps
}
