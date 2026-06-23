<script setup lang="ts">
import type { LeaveStatus } from './LeaveRequest'
import { LEAVE_STATUS_LABELS } from './LeaveRequest'

defineProps<{
  status: LeaveStatus
}>()

const styles: Record<LeaveStatus, string> = {
  pending: 'bg-amber-50 text-amber-700 ring-amber-200',
  approved: 'bg-emerald-50 text-emerald-700 ring-emerald-200',
  rejected: 'bg-rose-50 text-rose-700 ring-rose-200',
}

const dotStyles: Record<LeaveStatus, string> = {
  pending: 'bg-amber-500',
  approved: 'bg-emerald-500',
  rejected: 'bg-rose-500',
}
</script>

<template>
  <span
    class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ring-1 ring-inset"
    :class="styles[status]"
  >
    <span class="h-1.5 w-1.5 rounded-full" :class="dotStyles[status]" />
    {{ LEAVE_STATUS_LABELS[status] }}
  </span>
</template>
