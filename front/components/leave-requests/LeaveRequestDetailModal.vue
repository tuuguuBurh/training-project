<script setup lang="ts">
import CommonDraggableModal from '~/components/Common/DraggableModal.vue'
import CommonCopyableField from '~/components/Common/CopyableField.vue'
import LeaveStatusBadge from './LeaveStatusBadge.vue'
import LeaveTypeBadge from './LeaveTypeBadge.vue'
import { LEAVE_STATUS_LABELS, type LeaveRequest } from './LeaveRequest'

defineProps<{
  visible: boolean
  request: LeaveRequest | null
}>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
}>()

const { $toast } = useNuxtApp()

const dateFormatter = new Intl.DateTimeFormat('mn-MN', {
  weekday: 'long',
  day: '2-digit',
  month: 'long',
  year: 'numeric',
})

const dateTimeFormatter = new Intl.DateTimeFormat('mn-MN', {
  day: '2-digit',
  month: 'short',
  year: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
})

function initials(name: string) {
  return name
    .split(' ')
    .map((part) => part[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()
}

function handleCopy(text: string) {
  navigator.clipboard.writeText(text)
  $toast.success('Хууллаа')
}

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
  <CommonDraggableModal
    :visible="visible"
    :title="request ? `Чөлөөний дэлгэрэнгүй: ${request.employee.name}` : 'Ачааллаж байна...'"
    :hide-confirm="true"
    cancel-text="Хаах"
    width="640px"
    @update:visible="emit('update:visible', $event)"
  >
    <div v-if="request" class="space-y-6">
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

      <div class="grid grid-cols-2 gap-4">
        <CommonCopyableField label="Хүсэлтийн ID" :value="request.id" mono @copy="handleCopy" />
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
        <div v-if="request.description" class="col-span-2 space-y-1">
          <label class="block text-xs font-medium uppercase tracking-wide text-slate-500">Тайлбар</label>
          <p class="rounded-lg bg-slate-50 p-3 text-sm text-slate-700">{{ request.description }}</p>
        </div>
      </div>

      <div class="space-y-3 border-t border-slate-200 pt-4">
        <h4 class="text-sm font-semibold text-slate-900">Зөвшөөрөгчид</h4>
        <div class="space-y-2">
          <div
            v-for="approver in request.approvers"
            :key="approver.id"
            class="flex items-center justify-between rounded-lg border border-slate-200 px-3 py-2"
          >
            <div class="flex items-center gap-2">
              <div
                class="flex h-8 w-8 items-center justify-center rounded-full bg-slate-100 text-xs font-semibold text-slate-600"
              >
                {{ initials(approver.name) }}
              </div>
              <span class="text-sm font-medium text-slate-900">{{ approver.name }}</span>
            </div>
            <div class="text-right">
              <span class="text-xs font-medium text-slate-600">{{ LEAVE_STATUS_LABELS[approver.status] }}</span>
              <p v-if="approver.respondedAt" class="text-[11px] text-slate-400">
                {{ dateTimeFormatter.format(new Date(approver.respondedAt)) }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </CommonDraggableModal>
</template>
