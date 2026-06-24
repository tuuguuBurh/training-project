<script setup lang="ts">
import type { LeaveType } from '~/types/leave-request/leave-request-types'
import RecentApprovedLeaveDatePicker from './RecentApprovedLeaveDatePicker.vue'
import { dateRangeForPeriod } from './recent-approved-leaves-dates'
import {
  PERIOD_CHIP_LABELS,
  type RecentApprovedLeaveFilterState,
  type RecentApprovedLeavePeriod,
  type RecentApprovedLeaveSort,
} from './recent-approved-leaves-types'
import { ChevronDown, Search } from 'lucide-vue-next'

const props = defineProps<{
  modelValue: RecentApprovedLeaveFilterState
  leaveTypes: LeaveType[]
}>()

const emit = defineEmits<{
  'update:modelValue': [value: RecentApprovedLeaveFilterState]
}>()

const periodChips = Object.entries(PERIOD_CHIP_LABELS) as Array<[RecentApprovedLeavePeriod, string]>

const sortOptions: Array<{ value: RecentApprovedLeaveSort; label: string }> = [
  { value: 'newest', label: 'Шинэ' },
  { value: 'oldest', label: 'Хуучин' },
  { value: 'name', label: 'Нэр' },
]

const typeOptions = computed(() => [
  { value: 'all' as const, label: 'Бүгд' },
  ...props.leaveTypes.map((type) => ({ value: type.id, label: type.name })),
])

function update<K extends keyof RecentApprovedLeaveFilterState>(key: K, value: RecentApprovedLeaveFilterState[K]) {
  emit('update:modelValue', { ...props.modelValue, [key]: value })
}

function selectPeriod(period: RecentApprovedLeavePeriod) {
  const range = dateRangeForPeriod(period)
  emit('update:modelValue', {
    ...props.modelValue,
    period,
    startDate: range.startDate,
    endDate: range.endDate,
  })
}

function onCustomRange(range: { startDate: string; endDate: string }) {
  emit('update:modelValue', {
    ...props.modelValue,
    period: 'custom',
    startDate: range.startDate,
    endDate: range.endDate,
  })
}
</script>

<template>
  <div class="flex flex-col gap-4 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div class="flex flex-wrap items-center gap-2">
        <button
          v-for="[period, label] in periodChips"
          :key="period"
          type="button"
          class="rounded-full px-4 py-2 text-sm font-medium transition-colors"
          :class="
            modelValue.period === period
              ? 'bg-blue-600 text-white'
              : 'border border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
          "
          @click="selectPeriod(period)"
        >
          {{ label }}
        </button>
      </div>

      <RecentApprovedLeaveDatePicker
        :start-date="modelValue.startDate"
        :end-date="modelValue.endDate"
        @update:range="onCustomRange"
      />
    </div>

    <div class="h-px bg-slate-200" />

    <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
      <div class="relative min-w-0 flex-1">
        <Search class="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-slate-400" />
        <input
          type="text"
          :value="modelValue.search"
          class="w-full rounded-xl border border-slate-200 py-2.5 pl-10 pr-3 text-sm text-slate-900 placeholder:text-slate-400 transition-colors focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"
          placeholder="Нэр эсвэл имэйлээр хайх..."
          @input="update('search', ($event.target as HTMLInputElement).value)"
        />
      </div>

      <div class="flex shrink-0 flex-wrap items-center gap-2">
        <div class="relative">
          <select
            :value="modelValue.leaveTypeId"
            class="appearance-none rounded-lg border border-slate-200 bg-white py-2.5 pl-3 pr-8 text-sm text-slate-700 transition-colors focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"
            @change="update('leaveTypeId', ($event.target as HTMLSelectElement).value)"
          >
            <option v-for="opt in typeOptions" :key="opt.value" :value="opt.value">Төрөл: {{ opt.label }}</option>
          </select>
          <ChevronDown
            class="pointer-events-none absolute right-2.5 top-1/2 size-3.5 -translate-y-1/2 text-slate-400"
          />
        </div>

        <div class="relative">
          <select
            :value="modelValue.sort"
            class="appearance-none rounded-lg border border-slate-200 bg-white py-2.5 pl-3 pr-8 text-sm text-slate-700 transition-colors focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"
            @change="update('sort', ($event.target as HTMLSelectElement).value as RecentApprovedLeaveSort)"
          >
            <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">Эрэмбэ: {{ opt.label }}</option>
          </select>
          <ChevronDown
            class="pointer-events-none absolute right-2.5 top-1/2 size-3.5 -translate-y-1/2 text-slate-400"
          />
        </div>
      </div>
    </div>
  </div>
</template>
