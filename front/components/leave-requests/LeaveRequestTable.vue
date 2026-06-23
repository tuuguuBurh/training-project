<script setup lang="ts">
import type { LeaveRequest } from './LeaveRequest'
import LeaveTypeBadge from './LeaveTypeBadge.vue'
import LeaveStatusBadge from './LeaveStatusBadge.vue'
import LeaveApproversStack from './LeaveApproversStack.vue'

defineProps<{
  requests: LeaveRequest[]
  loading?: boolean
}>()

const emit = defineEmits<{
  'row-click': [request: LeaveRequest]
}>()

function initials(name: string) {
  return name
    .split(' ')
    .map((part) => part[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()
}

const dateFormatter = new Intl.DateTimeFormat('mn-MN', {
  day: '2-digit',
  month: 'short',
  year: 'numeric',
})
const dateTimeFormatter = new Intl.DateTimeFormat('mn-MN', {
  day: '2-digit',
  month: 'short',
  hour: '2-digit',
  minute: '2-digit',
})

function formatDate(value: string) {
  return dateFormatter.format(new Date(value))
}

function formatSubmitted(value: string) {
  return dateTimeFormatter.format(new Date(value))
}

function formatTimeRange(startTime: string, endTime: string) {
  return `${startTime} – ${endTime}`
}
</script>

<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-slate-200">
      <thead class="bg-slate-50">
        <tr>
          <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500 sm:pl-8">
            Ажилчин
          </th>
          <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">Төрөл</th>
          <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">Огноо / Цаг</th>
          <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">Төлөв</th>
          <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">Зөвшөөрөгчид</th>
          <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500 sm:pr-8">
            Илгээсэн
          </th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-100 bg-white">
        <tr v-if="loading">
          <td colspan="6" class="px-6 py-16 text-center text-sm text-slate-500">Ачааллаж байна...</td>
        </tr>

        <tr
          v-for="req in requests"
          v-else
          :key="req.id"
          class="cursor-pointer transition-colors hover:bg-slate-50"
          @click="emit('row-click', req)"
        >
          <td class="whitespace-nowrap px-6 py-4 sm:pl-8">
            <div class="flex items-center gap-3">
              <div
                class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-blue-100 text-xs font-semibold text-blue-700"
              >
                {{ initials(req.employee.name) }}
              </div>
              <div class="min-w-0">
                <p class="truncate text-sm font-medium text-slate-900">
                  {{ req.employee.name }}
                </p>
                <p class="truncate text-xs text-slate-500">
                  {{ req.employee.email }}
                </p>
              </div>
            </div>
          </td>

          <td class="whitespace-nowrap px-4 py-4">
            <LeaveTypeBadge :name="req.leaveType.name" />
          </td>

          <td class="whitespace-nowrap px-4 py-4">
            <p class="text-sm text-slate-900">{{ formatDate(req.startDate) }}</p>
            <p class="text-xs text-slate-500">{{ formatTimeRange(req.startTime, req.endTime) }}</p>
          </td>

          <td class="whitespace-nowrap px-4 py-4">
            <LeaveStatusBadge :status="req.status" />
          </td>

          <td class="whitespace-nowrap px-4 py-4">
            <LeaveApproversStack :approvers="req.approvers" />
          </td>

          <td class="whitespace-nowrap px-4 py-4 text-sm text-slate-500 sm:pr-8">
            {{ formatSubmitted(req.submittedAt) }}
          </td>
        </tr>

        <tr v-if="!loading && requests.length === 0">
          <td colspan="6" class="px-6 py-16 text-center">
            <p class="text-sm font-medium text-slate-900">Илэрц олдсонгүй</p>
            <p class="mt-1 text-sm text-slate-500">Шүүлтүүрээ өөрчилж дахин оролдоно уу.</p>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
