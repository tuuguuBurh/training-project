<script setup lang="ts">
import type { Approver } from './LeaveRequest'

const props = defineProps<{
  approvers: Approver[]
}>()

function initials(name: string) {
  return name
    .split(' ')
    .map((part) => part[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()
}

const ringStyles: Record<Approver['status'], string> = {
  approved: 'ring-emerald-500',
  rejected: 'ring-rose-500',
  pending: 'ring-slate-200',
}

const approvedCount = props.approvers.filter((a) => a.status === 'approved').length
</script>

<template>
  <div class="flex items-center gap-2">
    <div class="flex -space-x-2">
      <div v-for="approver in approvers" :key="approver.id" class="group relative">
        <div
          class="flex h-7 w-7 items-center justify-center rounded-full bg-slate-100 text-[10px] font-semibold text-slate-600 ring-2"
          :class="ringStyles[approver.status]"
        >
          {{ initials(approver.name) }}
        </div>
        <span
          v-if="approver.status === 'approved'"
          class="absolute -bottom-0.5 -right-0.5 flex h-3 w-3 items-center justify-center rounded-full bg-emerald-500 text-white ring-1 ring-white"
        >
          <svg class="h-2 w-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="4">
            <path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </span>
        <span
          v-else-if="approver.status === 'rejected'"
          class="absolute -bottom-0.5 -right-0.5 flex h-3 w-3 items-center justify-center rounded-full bg-rose-500 text-white ring-1 ring-white"
        >
          <svg class="h-2 w-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="4">
            <path d="M6 6l12 12M18 6L6 18" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </span>

        <!-- Tooltip -->
        <div
          class="pointer-events-none absolute -top-9 left-1/2 z-10 -translate-x-1/2 whitespace-nowrap rounded-md bg-slate-900 px-2 py-1 text-[11px] text-white opacity-0 transition-opacity group-hover:opacity-100"
        >
          {{ approver.name }}
        </div>
      </div>
    </div>
    <span class="text-xs text-slate-500">{{ approvedCount }}/{{ approvers.length }}</span>
  </div>
</template>
