<script setup lang="ts">
import type { LeaveDayGroup } from './useRecentApprovedLeaves'
import RecentApprovedLeaveItemRow from './RecentApprovedLeaveItemRow.vue'
import { RECENT_APPROVED_VISIBLE_COUNT } from './recent-approved-leaves-types'
import { ChevronDown } from 'lucide-vue-next'

const props = defineProps<{
  group: LeaveDayGroup
}>()

const expanded = ref(false)

const visibleRequests = computed(() => {
  if (expanded.value) {
    return props.group.requests
  }
  return props.group.requests.slice(0, RECENT_APPROVED_VISIBLE_COUNT)
})

const hiddenCount = computed(() => {
  return Math.max(0, props.group.requests.length - RECENT_APPROVED_VISIBLE_COUNT)
})

const showExpand = computed(() => !expanded.value && hiddenCount.value > 0)
</script>

<template>
  <section class="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
    <div class="flex items-start justify-between gap-4 border-b border-slate-100 bg-slate-50 px-5 py-4">
      <div>
        <h2 class="text-lg font-semibold text-slate-900">{{ group.label }}</h2>
        <p class="mt-0.5 text-sm text-slate-500">{{ group.subtitle }}</p>
      </div>
      <span
        class="inline-flex shrink-0 items-center gap-1.5 rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700"
      >
        <span class="h-1.5 w-1.5 rounded-full bg-emerald-500" />
        {{ group.requests.length }} хүн чөлөөтэй
      </span>
    </div>

    <ul class="divide-y divide-slate-100">
      <RecentApprovedLeaveItemRow v-for="request in visibleRequests" :key="request.id" :request="request" />
    </ul>

    <button
      v-if="showExpand"
      type="button"
      class="flex w-full items-center justify-center gap-1 border-t border-slate-100 px-5 py-3 text-sm font-medium text-blue-600 transition-colors hover:bg-slate-50"
      @click="expanded = true"
    >
      + Бусад {{ hiddenCount }} хүсэлтийг харах
      <ChevronDown class="size-4" />
    </button>
  </section>
</template>
