<script setup lang="ts">
import RecentApprovedLeavesHeader from './RecentApprovedLeavesHeader.vue'
import RecentApprovedLeaveFilterBar from './RecentApprovedLeaveFilterBar.vue'
import RecentApprovedLeaveGroupCard from './RecentApprovedLeaveGroupCard.vue'
import { useRecentApprovedLeaves } from './useRecentApprovedLeaves'

const { dayGroups, leaveTypes, filters, loading, error, fetchRecentApprovedLeaves, fetchLeaveTypes } =
  useRecentApprovedLeaves()

onMounted(() => {
  fetchLeaveTypes()
  fetchRecentApprovedLeaves()
})
</script>

<template>
  <div class="min-h-full w-full">
    <RecentApprovedLeavesHeader />

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
      <RecentApprovedLeaveFilterBar v-model="filters" :leave-types="leaveTypes" />

      <div
        v-if="loading"
        class="rounded-xl border border-slate-200 bg-white px-6 py-16 text-center text-sm text-slate-500"
      >
        Ачааллаж байна...
      </div>

      <template v-else>
        <div
          v-if="dayGroups.length === 0"
          class="rounded-xl border border-slate-200 bg-white px-6 py-16 text-center text-sm text-slate-500"
        >
          Чөлөөний хүсэлт олдсонгүй.
        </div>

        <RecentApprovedLeaveGroupCard v-for="group in dayGroups" :key="group.date" :group="group" />
      </template>
    </div>
  </div>
</template>
