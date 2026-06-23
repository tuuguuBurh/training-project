<script setup lang="ts">
import MyRequestFilters from './MyRequestFilters.vue'
import type { MyRequestFilterState } from './MyRequestFilters.vue'
import MyRequestTable from './MyRequestTable.vue'
import { useMyLeaveRequests } from './useMyLeaveRequests'
import LeaveRequestDetailModal from '~/components/leave-requests/LeaveRequestDetailModal.vue'
import type { LeaveRequest } from '~/components/leave-requests/LeaveRequest'
import { API_ENDPOINTS } from '~/constants'
import type { LeaveType } from '~/types/leave-request/leave-request-types'

const api = useApi()
const { leaveRequests, loading, error, fetchMyLeaveRequests } = useMyLeaveRequests()

const leaveTypes = ref<LeaveType[]>([])
const detailModalVisible = ref(false)
const selectedRequest = ref<LeaveRequest | null>(null)

const now = new Date()
const today = now.toISOString().slice(0, 10)
const currentMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`

const filters = ref<MyRequestFilterState>({
  status: 'all',
  leaveTypeId: 'all',
  filterMode: 'all',
  date: today,
  month: currentMonth,
})

async function loadLeaveTypes() {
  const { data } = await api.get<LeaveType[]>(API_ENDPOINTS.LEAVE_TYPES.LIST)
  leaveTypes.value = data || []
}

async function loadData() {
  if (filters.value.filterMode === 'month') {
    const [year, month] = filters.value.month.split('-').map(Number)
    await fetchMyLeaveRequests({ year, month })
    return
  }
  if (filters.value.filterMode === 'day') {
    await fetchMyLeaveRequests({ date: filters.value.date })
    return
  }
  await fetchMyLeaveRequests()
}

const filteredRequests = computed(() => {
  return leaveRequests.value.filter((req) => {
    if (filters.value.status !== 'all' && req.status !== filters.value.status) {
      return false
    }
    if (filters.value.leaveTypeId !== 'all' && req.leaveType.id !== filters.value.leaveTypeId) {
      return false
    }
    return true
  })
})

function handleRowClick(request: LeaveRequest) {
  selectedRequest.value = request
  detailModalVisible.value = true
}

function handleRequestUpdated(updated: LeaveRequest) {
  selectedRequest.value = updated
  const index = leaveRequests.value.findIndex((item) => item.id === updated.id)
  if (index !== -1) {
    leaveRequests.value[index] = updated
  }
}

watch(
  () => [filters.value.filterMode, filters.value.date, filters.value.month],
  () => {
    loadData()
  }
)

onMounted(async () => {
  await Promise.all([loadLeaveTypes(), loadData()])
})
</script>

<template>
  <div class="mt-2">
    <div class="mb-3 px-4">
      <h2 class="text-lg font-semibold text-slate-900">
        Миний чөлөөнүүд
        <span class="font-medium text-slate-400">({{ filteredRequests.length }})</span>
      </h2>
      <p class="mt-0.5 text-sm text-slate-500">Таны илгээсэн чөлөөний хүсэлтүүдийн түүх.</p>
    </div>

    <div class="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
      <MyRequestFilters v-model="filters" :leave-types="leaveTypes" />

      <div v-if="error" class="border-b border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
        {{ error }}
        <button type="button" class="ml-2 font-medium underline" @click="loadData">Дахин оролдох</button>
      </div>

      <MyRequestTable :requests="filteredRequests" :loading="loading" @row-click="handleRowClick" />
    </div>

    <LeaveRequestDetailModal
      v-model:visible="detailModalVisible"
      :request="selectedRequest"
      @updated="handleRequestUpdated"
    />
  </div>
</template>
