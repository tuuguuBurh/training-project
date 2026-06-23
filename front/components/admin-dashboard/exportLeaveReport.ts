import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'
import * as XLSX from 'xlsx'
import type { LeaveReportItem } from '~/types/admin/admin-types'
import { LEAVE_STATUS_LABELS, mapApiStatus } from '~/components/leave-requests/LeaveRequest'

function formatStatus(status: string): string {
  return LEAVE_STATUS_LABELS[mapApiStatus(status)]
}

function formatDate(value: string): string {
  return new Intl.DateTimeFormat('mn-MN', { year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date(value))
}

function toRows(items: LeaveReportItem[]) {
  return items.map((item) => [
    item.employee_name,
    item.leave_type,
    formatDate(item.start_date),
    formatDate(item.end_date),
    item.total_days,
    formatStatus(item.status),
  ])
}

export function exportLeaveReportExcel(items: LeaveReportItem[], filename = 'leave-report.xlsx') {
  const headers = ['Ажилтан', 'Чөлөөний төрөл', 'Эхлэх огноо', 'Дуусах огноо', 'Нийт өдөр', 'Төлөв']
  const worksheet = XLSX.utils.aoa_to_sheet([headers, ...toRows(items)])
  const workbook = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Leave Report')
  XLSX.writeFile(workbook, filename)
}

export function exportLeaveReportPdf(items: LeaveReportItem[], filename = 'leave-report.pdf') {
  const doc = new jsPDF({ orientation: 'landscape' })
  autoTable(doc, {
    head: [['Ажилтан', 'Чөлөөний төрөл', 'Эхлэх огноо', 'Дуусах огноо', 'Нийт өдөр', 'Төлөв']],
    body: toRows(items),
    styles: { fontSize: 9 },
    headStyles: { fillColor: [24, 119, 242] },
  })
  doc.save(filename)
}
