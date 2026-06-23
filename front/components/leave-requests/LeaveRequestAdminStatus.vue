<script setup lang="ts">
import LeaveStatusBadge from './LeaveStatusBadge.vue'
import { LEAVE_STATUS_LABELS, type LeaveRequest, type LeaveStatus } from './LeaveRequest'
import { dateTimeFormatter } from './leaveRequestFormatters'

const props = defineProps<{
  request: LeaveRequest
  submitting: boolean
}>()

const emit = defineEmits<{
  'update-status': [status: 'APPROVED' | 'REJECTED', comment: string]
}>()

const commentDraft = ref('')
const rejectError = ref('')

const statusOptions: Array<{ value: LeaveStatus; label: string }> = [
  { value: 'approved', label: LEAVE_STATUS_LABELS.approved },
  { value: 'rejected', label: LEAVE_STATUS_LABELS.rejected },
]

function handleStatusChange(status: 'APPROVED' | 'REJECTED') {
  if (status === 'REJECTED' && !commentDraft.value.trim()) {
    rejectError.value = 'Татгалзах үед тайлбар заавал оруулна'
    return
  }
  rejectError.value = ''
  emit('update-status', status, commentDraft.value.trim())
}

watch(
  () => props.request.id,
  () => {
    commentDraft.value = ''
    rejectError.value = ''
  }
)
</script>

<template>
  <div class="space-y-3 rounded-xl border border-indigo-200 bg-indigo-50/60 p-4">
    <div class="flex items-center justify-between gap-3">
      <div>
        <h4 class="text-sm font-semibold text-slate-900">Админы ерөнхий шийдвэр</h4>
        <p class="text-xs text-slate-500">Хүсэлтийн үндсэн төлөвийг өөрчлөх</p>
      </div>
      <LeaveStatusBadge :status="request.status" />
    </div>

    <div v-if="request.adminDecision?.rejectionReason" class="rounded-md bg-white px-3 py-2 text-xs text-rose-700">
      <span class="font-medium">Админы тайлбар:</span>
      {{ request.adminDecision.rejectionReason }}
      <p v-if="request.adminDecision.decidedAt" class="mt-1 text-[11px] text-slate-400">
        {{ request.adminDecision.name }} ·
        {{ dateTimeFormatter.format(new Date(request.adminDecision.decidedAt)) }}
      </p>
    </div>

    <div class="space-y-2">
      <label class="block text-xs font-medium uppercase tracking-wide text-slate-500">
        Тайлбар
        <span class="font-normal normal-case text-slate-400">(татгалзах үед заавал)</span>
      </label>
      <textarea
        v-model="commentDraft"
        rows="2"
        placeholder="Админы тайлбар..."
        class="w-full rounded-lg border border-slate-200 bg-white p-2 text-sm text-slate-700 focus:border-slate-400 focus:outline-none"
        :disabled="submitting"
      />
      <p v-if="rejectError" class="text-xs text-rose-600">{{ rejectError }}</p>
    </div>

    <div class="flex flex-wrap justify-end gap-2">
      <button
        v-for="option in statusOptions"
        :key="option.value"
        type="button"
        class="rounded-lg px-3 py-1.5 text-sm font-medium text-white disabled:opacity-50"
        :class="option.value === 'approved' ? 'bg-emerald-500 hover:bg-emerald-600' : 'bg-rose-500 hover:bg-rose-600'"
        :disabled="submitting || request.status === option.value"
        @click="handleStatusChange(option.value === 'approved' ? 'APPROVED' : 'REJECTED')"
      >
        {{ option.label }}
      </button>
    </div>
  </div>
</template>
