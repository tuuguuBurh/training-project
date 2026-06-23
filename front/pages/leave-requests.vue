<script setup lang="ts">
import LeaveRequestHeader from '~/components/leave-requests/LeaveRequestHeader.vue'
import LeaveRequestFilters from '~/components/leave-requests/LeaveRequestFilters.vue'
import LeaveRequestTable from '~/components/leave-requests/LeaveRequestTable.vue'
import LeaveRequestDetailModal from '~/components/leave-requests/LeaveRequestDetailModal.vue'
import type { LeaveFilterState } from '~/components/leave-requests/LeaveRequestFilters.vue'
import { useLeaveRequests } from '~/components/leave-requests/UseleaveRequests'
import { API_ENDPOINTS } from '~/constants'
import type { LeaveType } from '~/types/leave-request/leave-request-types'
import type { LeaveRequest } from '~/components/leave-requests/LeaveRequest'

definePageMeta({
  title: 'Чөлөөний хүсэлтүүд',
})

const api = useApi()
const { leaveRequests, loading, error, fetchLeaveRequests } = useLeaveRequests()

const leaveTypes = ref<LeaveType[]>([])
const detailModalVisible = ref(false)
const selectedRequest = ref<LeaveRequest | null>(null)

const now = new Date()
const today = now.toISOString().slice(0, 10)
const currentMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`

const filters = ref<LeaveFilterState>({
  search: '',
  status: 'all',
  leaveTypeId: 'all',
  filterMode: 'day',
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
    await fetchLeaveRequests({ year, month })
    return
  }
  await fetchLeaveRequests({ date: filters.value.date })
}

const filteredRequests = computed(() => {
  return leaveRequests.value.filter((req) => {
    if (filters.value.search) {
      const q = filters.value.search.trim().toLowerCase()
      const matchesName = req.employee.name.toLowerCase().includes(q)
      const matchesEmail = req.employee.email.toLowerCase().includes(q)
      if (!matchesName && !matchesEmail) return false
    }
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
  <div class="min-h-full w-full">
    <LeaveRequestHeader :total="filteredRequests.length" />
    <LeaveRequestFilters v-model="filters" :leave-types="leaveTypes" />

    <div
      v-if="error"
      class="mx-6 mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 sm:mx-8"
    >
      {{ error }}
      <button type="button" class="ml-2 font-medium underline" @click="loadData">Дахин оролдох</button>
    </div>

    <div class="px-6 py-6 sm:px-8">
      <div class="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
        <LeaveRequestTable :requests="filteredRequests" :loading="loading" @row-click="handleRowClick" />
      </div>
    </div>

    <LeaveRequestDetailModal v-model:visible="detailModalVisible" :request="selectedRequest" />
  </div>
</template>
