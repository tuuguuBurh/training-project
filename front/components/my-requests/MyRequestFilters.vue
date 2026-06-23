<script setup lang="ts">
import type { LeaveStatus } from '~/components/leave-requests/LeaveRequest'
import { LEAVE_STATUS_LABELS } from '~/components/leave-requests/LeaveRequest'
import type { LeaveType } from '~/types/leave-request/leave-request-types'

export interface MyRequestFilterState {
  status: LeaveStatus | 'all'
  leaveTypeId: string | 'all'
  filterMode: 'all' | 'day' | 'month'
  date: string
  month: string
}

const props = defineProps<{
  modelValue: MyRequestFilterState
  leaveTypes: LeaveType[]
}>()

const emit = defineEmits<{
  'update:modelValue': [value: MyRequestFilterState]
}>()

function update<K extends keyof MyRequestFilterState>(key: K, value: MyRequestFilterState[K]) {
  emit('update:modelValue', { ...props.modelValue, [key]: value })
}

const statusOptions: Array<{ value: LeaveStatus | 'all'; label: string }> = [
  { value: 'all', label: 'Бүгд' },
  { value: 'pending', label: LEAVE_STATUS_LABELS.pending },
  { value: 'approved', label: LEAVE_STATUS_LABELS.approved },
  { value: 'rejected', label: LEAVE_STATUS_LABELS.rejected },
]

const typeOptions = computed(() => [
  { value: 'all' as const, label: 'Бүх төрөл' },
  ...props.leaveTypes.map((type) => ({ value: type.id, label: type.name })),
])

const hasActiveFilters = computed(() => {
  return (
    props.modelValue.status !== 'all' || props.modelValue.leaveTypeId !== 'all' || props.modelValue.filterMode !== 'all'
  )
})

function resetFilters() {
  const now = new Date()
  emit('update:modelValue', {
    status: 'all',
    leaveTypeId: 'all',
    filterMode: 'all',
    date: now.toISOString().slice(0, 10),
    month: `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`,
  })
}

function onDateChange(value: string) {
  emit('update:modelValue', {
    ...props.modelValue,
    filterMode: 'day',
    date: value,
  })
}

function onMonthChange(value: string) {
  emit('update:modelValue', {
    ...props.modelValue,
    filterMode: 'month',
    month: value,
  })
}

function showAll() {
  emit('update:modelValue', {
    ...props.modelValue,
    filterMode: 'all',
  })
}
</script>

<template>
  <div class="flex flex-wrap items-center gap-3 border-b border-slate-200 bg-white px-4 py-4">
    <button
      type="button"
      class="rounded-lg border px-3 py-2 text-sm transition-colors"
      :class="
        modelValue.filterMode === 'all'
          ? 'border-blue-300 bg-blue-50 text-blue-700 ring-1 ring-blue-100'
          : 'border-slate-200 bg-slate-50 text-slate-900 hover:bg-white'
      "
      @click="showAll"
    >
      Бүгд
    </button>

    <input
      type="date"
      :value="modelValue.date"
      class="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-900 transition-colors focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-100"
      :class="modelValue.filterMode === 'day' ? 'border-blue-300 ring-1 ring-blue-100' : ''"
      title="Өдрөөр шүүх"
      @input="onDateChange(($event.target as HTMLInputElement).value)"
    />

    <input
      type="month"
      :value="modelValue.month"
      class="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-900 transition-colors focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-100"
      :class="modelValue.filterMode === 'month' ? 'border-blue-300 ring-1 ring-blue-100' : ''"
      title="Сараар шүүх"
      @input="onMonthChange(($event.target as HTMLInputElement).value)"
    />

    <div class="relative">
      <select
        :value="modelValue.status"
        class="appearance-none rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 pr-8 text-sm text-slate-900 transition-colors focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-100"
        @change="update('status', ($event.target as HTMLSelectElement).value as LeaveStatus | 'all')"
      >
        <option v-for="opt in statusOptions" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>
      <svg
        class="pointer-events-none absolute right-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-slate-400"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <path d="M6 9l6 6 6-6" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
    </div>

    <div class="relative">
      <select
        :value="modelValue.leaveTypeId"
        class="appearance-none rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 pr-8 text-sm text-slate-900 transition-colors focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-100"
        @change="update('leaveTypeId', ($event.target as HTMLSelectElement).value)"
      >
        <option v-for="opt in typeOptions" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>
      <svg
        class="pointer-events-none absolute right-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-slate-400"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <path d="M6 9l6 6 6-6" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
    </div>

    <button
      v-if="hasActiveFilters"
      type="button"
      class="rounded-lg px-3 py-2 text-sm font-medium text-slate-500 transition-colors hover:bg-slate-100 hover:text-slate-700"
      @click="resetFilters"
    >
      Шүүлтүүр арилгах
    </button>
  </div>
</template>
