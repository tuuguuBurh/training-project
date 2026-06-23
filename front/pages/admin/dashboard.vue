<script setup lang="ts">
import AdminLeaveReport from '~/components/admin-dashboard/AdminLeaveReport.vue'
import AdminLeaveTypeChart from '~/components/admin-dashboard/AdminLeaveTypeChart.vue'
import AdminMonthlyTrendChart from '~/components/admin-dashboard/AdminMonthlyTrendChart.vue'
import AdminStatsCards from '~/components/admin-dashboard/AdminStatsCards.vue'
import { useAdminDashboard } from '~/components/admin-dashboard/useAdminDashboard'
import { useAdminLeaveReport } from '~/components/admin-dashboard/useAdminLeaveReport'

definePageMeta({
  title: 'Admin Dashboard',
  middleware: 'admin',
})

const { stats, leaveTypeStats, monthlyTrend, loading, error, fetchDashboard } = useAdminDashboard()
const {
  filters,
  reportItems,
  employees,
  leaveTypes,
  loading: reportLoading,
  error: reportError,
  hasGenerated,
  fetchFilterOptions,
  generateReport,
} = useAdminLeaveReport()

onMounted(async () => {
  await Promise.all([fetchDashboard(), fetchFilterOptions()])
})
</script>

<template>
  <div class="min-h-full bg-slate-50">
    <div class="border-b border-slate-200 bg-white px-6 py-5 sm:px-8">
      <h1 class="text-2xl font-semibold text-slate-900">Admin Dashboard</h1>
      <p class="mt-1 text-sm text-slate-500">Чөлөөний хүсэлтийн нэгдсэн статистик болон тайлан</p>
    </div>

    <div class="space-y-6 px-6 py-6 sm:px-8">
      <div v-if="error" class="rounded-lg bg-rose-50 px-4 py-3 text-sm text-rose-700">
        {{ error }}
      </div>

      <AdminStatsCards :stats="stats" :loading="loading" />

      <div class="grid gap-6 xl:grid-cols-2">
        <AdminLeaveTypeChart :items="leaveTypeStats" :loading="loading" />
        <AdminMonthlyTrendChart :items="monthlyTrend" :loading="loading" />
      </div>

      <AdminLeaveReport
        :filters="filters"
        :items="reportItems"
        :employees="employees"
        :leave-types="leaveTypes"
        :loading="reportLoading"
        :error="reportError"
        :has-generated="hasGenerated"
        @update:filters="filters = $event"
        @generate="generateReport"
      />
    </div>
  </div>
</template>
