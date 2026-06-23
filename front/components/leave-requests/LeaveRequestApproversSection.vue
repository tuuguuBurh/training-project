<script setup lang="ts">
import LeaveRequestApproverCard from './LeaveRequestApproverCard.vue'
import type { Approver } from './LeaveRequest'

defineProps<{
  approvers: Approver[]
  submitting: boolean
  canActForApprover: (approver: Approver) => boolean
}>()

const emit = defineEmits<{
  approve: [approverId: string, comment: string]
  reject: [approverId: string, comment: string]
}>()
</script>

<template>
  <div class="space-y-3 border-t border-slate-200 pt-4">
    <h4 class="text-sm font-semibold text-slate-900">Зөвшөөрөгчид</h4>
    <div class="space-y-3">
      <LeaveRequestApproverCard
        v-for="approver in approvers"
        :key="approver.id"
        :approver="approver"
        :can-act="canActForApprover(approver)"
        :submitting="submitting"
        @approve="emit('approve', approver.approverId, $event)"
        @reject="emit('reject', approver.approverId, $event)"
      />
    </div>
  </div>
</template>
