<script setup lang="ts">
import LeaveStatusBadge from '~/components/leave-requests/LeaveStatusBadge.vue'
import { mapApiStatus } from '~/components/leave-requests/LeaveRequest'
import { exportLeaveReportExcel, exportLeaveReportPdf } from '~/components/admin-dashboard/exportLeaveReport'
import type { AdminEmployee, LeaveReportFilters, LeaveReportItem } from '~/types/admin/admin-types'
import type { LeaveType } from '~/types/leave-request/leave-request-types'

const props = defineProps<{
  filters: LeaveReportFilters
  items: LeaveReportItem[]
  employees: AdminEmployee[]
  leaveTypes: LeaveType[]
  loading: boolean
  error: string | null
  hasGenerated: boolean
}>()

const emit = defineEmits<{
  'update:filters': [value: LeaveReportFilters]
  generate: []
}>()

const statusOptions = [
  { value: 'all', label: 'Бүгд' },
  { value: 'PENDING', label: 'Хүлээгдэж буй' },
  { value: 'APPROVED', label: 'Зөвшөөрсөн' },
  { value: 'REJECTED', label: 'Татгалзсан' },
]

function updateFilter<K extends keyof LeaveReportFilters>(key: K, value: LeaveReportFilters[K]) {
  emit('update:filters', { ...props.filters, [key]: value })
}

function formatDate(value: string): string {
  return new Intl.DateTimeFormat('mn-MN', { year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date(value))
}

function handleExportExcel() {
  if (!props.items.length) return
  exportLeaveReportExcel(props.items)
}

function handleExportPdf() {
  if (!props.items.length) return
  exportLeaveReportPdf(props.items)
}
</script>

<template>
  <div class="rounded-xl border border-slate-200 bg-white shadow-sm">
    <div class="border-b border-slate-200 px-6 py-4">
      <h3 class="text-lg font-semibold text-slate-900">Чөлөөний тайлан</h3>
      <p class="mt-1 text-sm text-slate-500">Шүүлтүүр сонгоод тайлан үүсгэнэ үү</p>
    </div>

    <div class="grid gap-4 border-b border-slate-200 px-6 py-5 md:grid-cols-2 xl:grid-cols-5">
      <label class="block space-y-1.5">
        <span class="text-sm font-medium text-slate-700">Эхлэх огноо</span>
        <input
          type="date"
          class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"
          :value="filters.fromDate"
          @input="updateFilter('fromDate', ($event.target as HTMLInputElement).value)"
        />
      </label>

      <label class="block space-y-1.5">
        <span class="text-sm font-medium text-slate-700">Дуусах огноо</span>
        <input
          type="date"
          class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"
          :value="filters.toDate"
          @input="updateFilter('toDate', ($event.target as HTMLInputElement).value)"
        />
      </label>

      <label class="block space-y-1.5">
        <span class="text-sm font-medium text-slate-700">Ажилтан</span>
        <select
          class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"
          :value="filters.employeeId"
          @change="updateFilter('employeeId', ($event.target as HTMLSelectElement).value)"
        >
          <option value="all">Бүгд</option>
          <option v-for="employee in employees" :key="employee.id" :value="employee.id">
            {{ employee.name }}
          </option>
        </select>
      </label>

      <label class="block space-y-1.5">
        <span class="text-sm font-medium text-slate-700">Чөлөөний төрөл</span>
        <select
          class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"
          :value="filters.leaveTypeId"
          @change="updateFilter('leaveTypeId', ($event.target as HTMLSelectElement).value)"
        >
          <option value="all">Бүх төрөл</option>
          <option v-for="type in leaveTypes" :key="type.id" :value="type.id">
            {{ type.name }}
          </option>
        </select>
      </label>

      <label class="block space-y-1.5">
        <span class="text-sm font-medium text-slate-700">Төлөв</span>
        <select
          class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"
          :value="filters.status"
          @change="updateFilter('status', ($event.target as HTMLSelectElement).value)"
        >
          <option v-for="option in statusOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </label>
    </div>

    <div class="flex flex-wrap items-center gap-3 px-6 py-4">
      <Button label="Тайлан үүсгэх" icon="pi pi-search" :loading="loading" @click="emit('generate')" />
      <Button
        label="Excel"
        icon="pi pi-file-excel"
        severity="secondary"
        outlined
        :disabled="!items.length"
        @click="handleExportExcel"
      />
      <Button
        label="PDF"
        icon="pi pi-file-pdf"
        severity="secondary"
        outlined
        :disabled="!items.length"
        @click="handleExportPdf"
      />
    </div>

    <div v-if="error" class="px-6 pb-4">
      <p class="rounded-lg bg-rose-50 px-4 py-3 text-sm text-rose-700">{{ error }}</p>
    </div>

    <div class="px-6 pb-6">
      <div v-if="loading" class="flex items-center justify-center py-16">
        <i class="pi pi-spin pi-spinner text-2xl text-blue-500" />
      </div>

      <div
        v-else-if="hasGenerated && items.length === 0"
        class="rounded-lg border border-dashed border-slate-200 py-16 text-center text-sm text-slate-500"
      >
        Тайлангийн мэдээлэл олдсонгүй
      </div>

      <div v-else-if="items.length > 0" class="overflow-x-auto rounded-lg border border-slate-200">
        <table class="min-w-full divide-y divide-slate-200 text-sm">
          <thead class="bg-slate-50">
            <tr>
              <th class="px-4 py-3 text-left font-semibold text-slate-700">Ажилтан</th>
              <th class="px-4 py-3 text-left font-semibold text-slate-700">Чөлөөний төрөл</th>
              <th class="px-4 py-3 text-left font-semibold text-slate-700">Эхлэх огноо</th>
              <th class="px-4 py-3 text-left font-semibold text-slate-700">Дуусах огноо</th>
              <th class="px-4 py-3 text-left font-semibold text-slate-700">Нийт өдөр</th>
              <th class="px-4 py-3 text-left font-semibold text-slate-700">Төлөв</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 bg-white">
            <tr v-for="item in items" :key="item.id" class="hover:bg-slate-50">
              <td class="px-4 py-3 text-slate-900">{{ item.employee_name }}</td>
              <td class="px-4 py-3 text-slate-700">{{ item.leave_type }}</td>
              <td class="px-4 py-3 text-slate-700">{{ formatDate(item.start_date) }}</td>
              <td class="px-4 py-3 text-slate-700">{{ formatDate(item.end_date) }}</td>
              <td class="px-4 py-3 text-slate-700">{{ item.total_days }}</td>
              <td class="px-4 py-3">
                <LeaveStatusBadge :status="mapApiStatus(item.status)" />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
