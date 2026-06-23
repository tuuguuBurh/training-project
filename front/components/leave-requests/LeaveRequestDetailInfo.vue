<script setup lang="ts">
import CommonCopyableField from '~/components/Common/CopyableField.vue'
import LeaveTypeBadge from './LeaveTypeBadge.vue'
import { dateFormatter, dateTimeFormatter } from './leaveRequestFormatters'
import type { LeaveRequest } from './LeaveRequest'

defineProps<{
  request: LeaveRequest
  showDescription: boolean
}>()

const emit = defineEmits<{
  copy: [text: string]
}>()
</script>

<template>
  <div class="grid grid-cols-2 gap-4">
    <CommonCopyableField label="Хүсэлтийн ID" :value="request.id" mono @copy="emit('copy', $event)" />
    <div class="space-y-1">
      <label class="block text-xs font-medium uppercase tracking-wide text-slate-500">Чөлөөний төрөл</label>
      <LeaveTypeBadge :name="request.leaveType.name" />
    </div>
    <div class="space-y-1">
      <label class="block text-xs font-medium uppercase tracking-wide text-slate-500">Огноо</label>
      <span class="text-sm font-medium text-slate-900">
        {{ dateFormatter.format(new Date(request.startDate)) }}
      </span>
    </div>
    <div class="space-y-1">
      <label class="block text-xs font-medium uppercase tracking-wide text-slate-500">Цаг</label>
      <span class="text-sm font-medium text-slate-900">{{ request.startTime }} – {{ request.endTime }}</span>
    </div>
    <div class="col-span-2 space-y-1">
      <label class="block text-xs font-medium uppercase tracking-wide text-slate-500">Илгээсэн</label>
      <span class="text-sm text-slate-700">{{ dateTimeFormatter.format(new Date(request.submittedAt)) }}</span>
    </div>
    <div v-if="showDescription && request.description" class="col-span-2 space-y-1">
      <label class="block text-xs font-medium uppercase tracking-wide text-slate-500">Хүсэлтийн тайлбар</label>
      <p class="rounded-lg bg-slate-50 p-3 text-sm text-slate-700">{{ request.description }}</p>
    </div>
  </div>
</template>
