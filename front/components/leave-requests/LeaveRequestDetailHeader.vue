<script setup lang="ts">
import LeaveStatusBadge from './LeaveStatusBadge.vue'
import { initials } from './leaveRequestFormatters'
import type { LeaveRequest } from './LeaveRequest'

defineProps<{
  request: LeaveRequest
}>()

const statusBannerClass: Record<LeaveRequest['status'], string> = {
  approved: 'bg-emerald-50 border border-emerald-200',
  pending: 'bg-amber-50 border border-amber-200',
  rejected: 'bg-rose-50 border border-rose-200',
}

const avatarClass: Record<LeaveRequest['status'], string> = {
  approved: 'bg-emerald-500',
  pending: 'bg-amber-500',
  rejected: 'bg-rose-500',
}
</script>

<template>
  <div class="rounded-xl p-4 flex items-center justify-between" :class="statusBannerClass[request.status]">
    <div class="flex items-center gap-3">
      <div
        class="flex h-12 w-12 items-center justify-center rounded-full text-lg font-bold text-white"
        :class="avatarClass[request.status]"
      >
        {{ initials(request.employee.name) }}
      </div>
      <div>
        <h3 class="font-semibold text-slate-900">{{ request.employee.name }}</h3>
        <p class="text-sm text-slate-600">{{ request.employee.email }}</p>
      </div>
    </div>
    <LeaveStatusBadge :status="request.status" />
  </div>
</template>
