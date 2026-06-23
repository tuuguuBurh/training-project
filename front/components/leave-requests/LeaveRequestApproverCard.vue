<script setup lang="ts">
import { LEAVE_STATUS_LABELS, type Approver } from './LeaveRequest'
import { dateTimeFormatter, initials } from './leaveRequestFormatters'

const props = defineProps<{
  approver: Approver
  canAct: boolean
  submitting: boolean
}>()

const emit = defineEmits<{
  approve: [comment: string]
  reject: [comment: string]
}>()

const commentDraft = ref('')
const rejectError = ref('')

function handleApprove() {
  rejectError.value = ''
  emit('approve', commentDraft.value)
}

function handleReject() {
  if (!commentDraft.value.trim()) {
    rejectError.value = 'Татгалзах үед тайлбар заавал оруулна'
    return
  }
  rejectError.value = ''
  emit('reject', commentDraft.value.trim())
}

watch(
  () => props.approver.id,
  () => {
    commentDraft.value = ''
    rejectError.value = ''
  }
)
</script>

<template>
  <div class="rounded-lg border border-slate-200 px-3 py-2">
    <div class="flex items-center justify-between">
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

    <div v-if="approver.rejectionReason" class="mt-2 rounded-md bg-rose-50 px-2.5 py-2 text-xs text-rose-700">
      <span class="font-medium">Тайлбар:</span> {{ approver.rejectionReason }}
    </div>

    <div v-if="canAct && approver.status === 'pending'" class="mt-3 space-y-2 border-t border-slate-100 pt-3">
      <label class="block text-xs font-medium uppercase tracking-wide text-slate-500">
        Тайлбар
        <span class="font-normal normal-case text-slate-400">(татгалзах үед заавал)</span>
      </label>
      <textarea
        v-model="commentDraft"
        rows="2"
        placeholder="Тайлбар бичих..."
        class="w-full rounded-lg border border-slate-200 p-2 text-sm text-slate-700 focus:border-slate-400 focus:outline-none"
        :disabled="submitting"
      />
      <p v-if="rejectError" class="text-xs text-rose-600">{{ rejectError }}</p>
      <div class="flex justify-end gap-2">
        <button
          type="button"
          class="rounded-lg bg-rose-500 px-3 py-1.5 text-sm font-medium text-white hover:bg-rose-600 disabled:opacity-50"
          :disabled="submitting"
          @click="handleReject"
        >
          Татгалзах
        </button>
        <button
          type="button"
          class="rounded-lg bg-emerald-500 px-3 py-1.5 text-sm font-medium text-white hover:bg-emerald-600 disabled:opacity-50"
          :disabled="submitting"
          @click="handleApprove"
        >
          Зөвшөөрөх
        </button>
      </div>
    </div>
  </div>
</template>
