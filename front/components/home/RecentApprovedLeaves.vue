<script setup lang="ts">
import LeaveTypeBadge from '~/components/leave-requests/LeaveTypeBadge.vue'
import { initials } from '~/components/leave-requests/leaveRequestFormatters'
import { RECENT_APPROVED_DAYS, useRecentApprovedLeaves } from './useRecentApprovedLeaves'

const { dayGroups, loading, error, fetchRecentApprovedLeaves } = useRecentApprovedLeaves()

function formatTimeRange(startTime: string, endTime: string) {
  return `${startTime} – ${endTime}`
}

onMounted(() => {
  fetchRecentApprovedLeaves()
})
</script>

<template>
  <div class="min-h-full w-full">
    <div class="border-b border-slate-200 bg-white px-6 py-6 sm:px-8">
      <h1 class="text-2xl font-semibold text-slate-900">Сүүлийн {{ RECENT_APPROVED_DAYS }} хоногийн чөлөө</h1>
      <p class="mt-1 text-sm text-slate-500">Зөвхөн зөвшөөрөгдсөн чөлөөний хүсэлтүүд</p>
    </div>

    <div
      v-if="error"
      class="mx-6 mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 sm:mx-8"
    >
      {{ error }}
      <button type="button" class="ml-2 font-medium underline" @click="fetchRecentApprovedLeaves()">
        Дахин оролдох
      </button>
    </div>

    <div class="space-y-6 px-6 py-6 sm:px-8">
      <div
        v-if="loading"
        class="rounded-xl border border-slate-200 bg-white px-6 py-16 text-center text-sm text-slate-500"
      >
        Ачааллаж байна...
      </div>

      <template v-else>
        <section
          v-for="group in dayGroups"
          :key="group.date"
          class="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm"
        >
          <div class="border-b border-slate-100 bg-slate-50 px-5 py-4">
            <h2 class="text-lg font-semibold text-slate-900">{{ group.label }}</h2>
            <p class="mt-0.5 text-sm text-slate-500">{{ group.subtitle }}</p>
          </div>

          <div v-if="group.requests.length === 0" class="px-5 py-8 text-sm text-slate-500">
            Энэ өдөр чөлөө авсан хүн байхгүй.
          </div>

          <ul v-else class="divide-y divide-slate-100">
            <li
              v-for="request in group.requests"
              :key="request.id"
              class="flex flex-col gap-3 px-5 py-4 sm:flex-row sm:items-center sm:justify-between"
            >
              <div class="flex min-w-0 items-center gap-3">
                <div
                  class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-emerald-100 text-sm font-semibold text-emerald-700"
                >
                  {{ initials(request.employee.name) }}
                </div>
                <div class="min-w-0">
                  <p class="truncate text-sm font-medium text-slate-900">{{ request.employee.name }}</p>
                  <p class="truncate text-xs text-slate-500">{{ request.employee.email }}</p>
                </div>
              </div>

              <div class="flex flex-wrap items-center gap-3 sm:justify-end">
                <LeaveTypeBadge :name="request.leaveType.name" />
                <span class="text-sm text-slate-600">{{ formatTimeRange(request.startTime, request.endTime) }}</span>
              </div>
            </li>
          </ul>
        </section>
      </template>
    </div>
  </div>
</template>
