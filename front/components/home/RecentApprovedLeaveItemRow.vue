<script setup lang="ts">
import LeaveTypeBadge from '~/components/leave-requests/LeaveTypeBadge.vue'
import { initials } from '~/components/leave-requests/leaveRequestFormatters'
import type { LeaveRequest } from '~/components/leave-requests/LeaveRequest'

defineProps<{
  request: LeaveRequest
}>()

function formatTimeRange(startTime: string, endTime: string) {
  return `${startTime} – ${endTime}`
}
</script>

<template>
  <li class="grid grid-cols-1 items-center gap-3 px-5 py-4 sm:grid-cols-[1fr_auto_auto] sm:gap-4">
    <div class="flex min-w-0 items-center gap-3">
      <div
        class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-emerald-100 text-sm font-semibold text-emerald-700"
      >
        {{ initials(request.employee.name) }}
      </div>
      <div class="min-w-0">
        <p class="truncate text-sm font-medium text-slate-900">{{ request.employee.name }}</p>
        <p class="truncate text-xs text-slate-500">{{ request.employee.email }}</p>
      </div>
    </div>

    <div class="shrink-0 sm:justify-self-center">
      <LeaveTypeBadge :name="request.leaveType.name" />
    </div>

    <span class="shrink-0 text-sm text-slate-600 sm:justify-self-end">
      {{ formatTimeRange(request.startTime, request.endTime) }}
    </span>
  </li>
</template>
