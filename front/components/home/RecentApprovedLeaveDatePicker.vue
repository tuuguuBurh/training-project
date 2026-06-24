<script setup lang="ts">
import { formatDateRangeLabel, normalizeDateRange } from './recent-approved-leaves-dates'
import { Calendar, ChevronDown } from 'lucide-vue-next'
import { onClickOutside } from '@vueuse/core'

const props = defineProps<{
  startDate: string
  endDate: string
}>()

const emit = defineEmits<{
  'update:range': [value: { startDate: string; endDate: string }]
}>()

const open = ref(false)
const rootRef = ref<HTMLElement | null>(null)

const draftStart = ref(props.startDate)
const draftEnd = ref(props.endDate)

const label = computed(() => formatDateRangeLabel(props.startDate, props.endDate))

watch(
  () => [props.startDate, props.endDate],
  ([start, end]) => {
    draftStart.value = start
    draftEnd.value = end
  }
)

onClickOutside(rootRef, () => {
  open.value = false
})

function toggleOpen() {
  if (!open.value) {
    draftStart.value = props.startDate
    draftEnd.value = props.endDate
  }
  open.value = !open.value
}

function applyRange() {
  const range = normalizeDateRange(draftStart.value, draftEnd.value)
  emit('update:range', range)
  open.value = false
}

function onStartChange(value: string) {
  draftStart.value = value
  if (value > draftEnd.value) {
    draftEnd.value = value
  }
}

function onEndChange(value: string) {
  draftEnd.value = value
  if (value < draftStart.value) {
    draftStart.value = value
  }
}
</script>

<template>
  <div ref="rootRef" class="relative">
    <button
      type="button"
      class="inline-flex items-center gap-2 rounded-lg border px-4 py-2 text-sm font-medium transition-colors"
      :class="
        open
          ? 'border-blue-300 bg-blue-50 text-blue-700 ring-1 ring-blue-100'
          : 'border-slate-200 text-slate-700 hover:bg-slate-50'
      "
      @click="toggleOpen"
    >
      <Calendar class="size-4 text-slate-500" />
      {{ label }}
      <ChevronDown class="size-4 text-slate-500 transition-transform" :class="open ? 'rotate-180' : ''" />
    </button>

    <div v-if="open" class="absolute right-0 z-20 mt-2 w-72 rounded-xl border border-slate-200 bg-white p-4 shadow-lg">
      <p class="mb-3 text-sm font-medium text-slate-900">Хугацаа сонгох</p>

      <div class="space-y-3">
        <label class="block">
          <span class="mb-1 block text-xs text-slate-500">Эхлэх</span>
          <input
            type="date"
            :value="draftStart"
            :max="draftEnd"
            class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 transition-colors focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"
            @input="onStartChange(($event.target as HTMLInputElement).value)"
          />
        </label>

        <label class="block">
          <span class="mb-1 block text-xs text-slate-500">Дуусах</span>
          <input
            type="date"
            :value="draftEnd"
            :min="draftStart"
            class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 transition-colors focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"
            @input="onEndChange(($event.target as HTMLInputElement).value)"
          />
        </label>
      </div>

      <button
        type="button"
        class="mt-4 w-full rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700"
        @click="applyRange"
      >
        Хэрэглэх
      </button>
    </div>
  </div>
</template>
