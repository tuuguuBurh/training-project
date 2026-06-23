<script setup lang="ts">
import CommonDraggableModal from '~/components/Common/DraggableModal.vue'
import LeaveRequestDetailHeader from './LeaveRequestDetailHeader.vue'
import LeaveRequestDetailInfo from './LeaveRequestDetailInfo.vue'
import LeaveRequestApproversSection from './LeaveRequestApproversSection.vue'
import LeaveRequestAdminStatus from './LeaveRequestAdminStatus.vue'
import { useLeaveRequestActions } from './useLeaveRequestActions'
import { useLeaveRequestDetail } from './useLeaveRequestDetail'
import type { LeaveRequest } from './LeaveRequest'

const props = defineProps<{
  visible: boolean
  request: LeaveRequest | null
}>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
  updated: [request: LeaveRequest]
}>()

const { $toast } = useNuxtApp()
const requestRef = computed(() => props.request)
const { isAdmin, canViewDescription, isCurrentApprover } = useLeaveRequestDetail(requestRef)
const { submitting, submitApproverDecision, submitAdminStatus } = useLeaveRequestActions()

function handleCopy(text: string) {
  navigator.clipboard.writeText(text)
  $toast.success('Хууллаа')
}

function canActForApprover(approver: LeaveRequest['approvers'][number]) {
  return isCurrentApprover(approver)
}

async function handleApproverApprove(_approverId: string, comment: string) {
  if (!props.request) return
  const updated = await submitApproverDecision(props.request.id, 'APPROVED', comment)
  if (updated) emit('updated', updated)
}

async function handleApproverReject(_approverId: string, comment: string) {
  if (!props.request) return
  const updated = await submitApproverDecision(props.request.id, 'REJECTED', comment)
  if (updated) emit('updated', updated)
}

async function handleAdminStatus(status: 'APPROVED' | 'REJECTED', comment: string) {
  if (!props.request) return
  const updated = await submitAdminStatus(props.request.id, status, comment)
  if (updated) emit('updated', updated)
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
      <LeaveRequestDetailHeader :request="request" />
      <LeaveRequestDetailInfo :request="request" :show-description="canViewDescription" @copy="handleCopy" />
      <LeaveRequestAdminStatus
        v-if="isAdmin"
        :request="request"
        :submitting="submitting"
        @update-status="handleAdminStatus"
      />
      <LeaveRequestApproversSection
        :approvers="request.approvers"
        :submitting="submitting"
        :can-act-for-approver="canActForApprover"
        @approve="handleApproverApprove"
        @reject="handleApproverReject"
      />
    </div>
  </CommonDraggableModal>
</template>
