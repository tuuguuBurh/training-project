<script setup lang="ts">
import type { LeaveStatus } from './LeaveRequest'
import { LEAVE_STATUS_LABELS } from './LeaveRequest'
import type { LeaveType } from '~/types/leave-request/leave-request-types'

export interface LeaveFilterState {
  search: string
  status: LeaveStatus | 'all'
  leaveTypeId: string | 'all'
  filterMode: 'day' | 'month'
  date: string
  month: string
}

const props = defineProps<{
  modelValue: LeaveFilterState
  leaveTypes: LeaveType[]
}>()

const emit = defineEmits<{
  'update:modelValue': [value: LeaveFilterState]
}>()

function update<K extends keyof LeaveFilterState>(key: K, value: LeaveFilterState[K]) {
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

const todayIso = () => new Date().toISOString().slice(0, 10)

const hasActiveFilters = computed(() => {
  return (
    props.modelValue.search !== '' ||
    props.modelValue.status !== 'all' ||
    props.modelValue.leaveTypeId !== 'all' ||
    props.modelValue.filterMode !== 'day' ||
    props.modelValue.date !== todayIso()
  )
})

function resetFilters() {
  const now = new Date()
  emit('update:modelValue', {
    search: '',
    status: 'all',
    leaveTypeId: 'all',
    filterMode: 'day',
    date: todayIso(),
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
</script>

<template>
  <div class="border-b border-slate-200 bg-white">
    <div class="flex flex-wrap items-center gap-3 px-6 py-4 sm:px-8">
      <div class="relative min-w-[220px] flex-1 sm:max-w-xs">
        <svg
          class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <circle cx="11" cy="11" r="7" />
          <path d="M21 21l-4.3-4.3" stroke-linecap="round" />
        </svg>
        <input
          type="text"
          :value="modelValue.search"
          class="w-full rounded-lg border border-slate-200 bg-slate-50 py-2 pl-9 pr-3 text-sm text-slate-900 placeholder:text-slate-400 transition-colors focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-100"
          placeholder="Нэр, имэйлээр хайх"
          @input="update('search', ($event.target as HTMLInputElement).value)"
        />
      </div>

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
  </div>
</template>
