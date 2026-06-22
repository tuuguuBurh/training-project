<script setup lang="ts">
import LeaveRequestHeader from '~/components/new-requests/Leaverequestheader.vue'
import LeaveRequestBody from '~/components/new-requests/Leaverequestbody.vue'
import LeaveRequestFooter from '~/components/new-requests/Leaverequestfooter.vue'
import type { LeaveRequestFormState } from '~/types/leave-request/leave-request-types'

const {
  leaveTypes,
  teamMembers,
  form,
  errors,
  times,
  loading,
  submitting,
  submitted,
  loadError,
  requestedHours,
  timeRangeInvalid,
  canSubmit,
  loadFormData,
  submit,
} = useLeaveRequestForm()

const balances = [
  { label: 'Ээлжийн амралт', value: 12 },
  { label: 'Өвчтэй', value: 5 },
  { label: 'Чөлөө', value: 3 },
]

function updateForm(next: LeaveRequestFormState) {
  Object.assign(form, next)
}
</script>

<template>
  <div class="min-h-full w-full">
    <div class="bg-white border-b border-slate-200">
      <div class="max-w-screen-2xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <h1 class="text-xl font-bold text-slate-900">Чөлөөний хүсэлт илгээх</h1>
      </div>
    </div>

    <div class="w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div v-if="loading" class="w-full bg-white border border-slate-200 rounded-2xl p-8 text-center text-slate-500">
        Мэдээлэл ачааллаж байна...
      </div>

      <div v-else-if="loadError" class="w-full bg-white border border-red-200 rounded-2xl p-8 text-center">
        <p class="text-red-600 mb-4">{{ loadError }}</p>
        <button
          type="button"
          class="rounded-lg bg-teal-700 px-4 py-2 text-sm font-semibold text-white hover:bg-teal-800"
          @click="loadFormData"
        >
          Дахин оролдох
        </button>
      </div>

      <form
        v-else
        class="w-full bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm"
        @submit.prevent="submit"
      >
        <LeaveRequestHeader :balances="balances" />

        <LeaveRequestBody
          :form="form"
          :leave-types="leaveTypes"
          :times="times"
          :team-members="teamMembers"
          :leave-type-error="errors.leaveTypeId"
          :approver-error="errors.approverIds"
          :time-range-invalid="timeRangeInvalid"
          :requested-hours="requestedHours"
          @update:form="updateForm"
        />

        <LeaveRequestFooter :submitted="submitted" :disabled="!canSubmit || submitting" :loading="submitting" />
      </form>
    </div>
  </div>
</template>
