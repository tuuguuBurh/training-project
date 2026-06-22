<script setup lang="ts">
import { ref, computed } from 'vue'
import { ChevronDown, Calendar } from 'lucide-vue-next'
import type { LeaveRequestFormState, LeaveType, TeamMember } from '~/types/leave-request/leave-request-types'

const props = defineProps<{
  form: LeaveRequestFormState
  leaveTypes: LeaveType[]
  times: string[]
  teamMembers: TeamMember[]
  leaveTypeError: boolean
  approverError: boolean
  timeRangeInvalid: boolean
  requestedHours: number
}>()

const emit = defineEmits<{
  'update:form': [value: LeaveRequestFormState]
}>()

const teamOpen = ref(false)
const teamWrapperRef = ref<HTMLElement | null>(null)

function toggleMember(id: string) {
  const i = props.form.approverIds.indexOf(id)
  const next = [...props.form.approverIds]
  if (i === -1) next.push(id)
  else next.splice(i, 1)
  emit('update:form', { ...props.form, approverIds: next })
}

const membersLabel = computed(() => {
  if (!props.form.approverIds.length) return 'Багийн гишүүд сонгох'

  const names = props.teamMembers
    .filter((member) => props.form.approverIds.includes(member.id))
    .map((member) => member.name)

  return names.join(', ')
})

function updateField<K extends keyof LeaveRequestFormState>(key: K, value: LeaveRequestFormState[K]) {
  emit('update:form', { ...props.form, [key]: value })
}

function handleClickOutside(e: MouseEvent) {
  if (teamWrapperRef.value && !teamWrapperRef.value.contains(e.target as Node)) {
    teamOpen.value = false
  }
}
</script>

<template>
  <div @click="handleClickOutside">
    <div class="mb-5">
      <label class="block text-sm font-semibold text-slate-700 mb-2">Чөлөөний төрөл</label>
      <div class="relative">
        <select
          :value="form.leaveTypeId"
          class="w-full appearance-none rounded-xl border bg-white px-4 py-3 text-sm text-slate-700 outline-none focus:ring-2 focus:ring-teal-500/40 focus:border-teal-500"
          :class="leaveTypeError ? 'border-red-400' : 'border-slate-200'"
          @change="updateField('leaveTypeId', ($event.target as HTMLSelectElement).value)"
        >
          <option value="" disabled>Чөлөөний төрөл сонгох</option>
          <option v-for="t in leaveTypes" :key="t.id" :value="t.id">
            {{ t.name }}
          </option>
        </select>
        <ChevronDown class="w-4 h-4 text-slate-400 absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none" />
      </div>
      <p v-if="leaveTypeError" class="text-xs text-red-500 mt-1.5">Чөлөөний төрөл сонгоно уу.</p>
    </div>

    <div class="mb-5">
      <label class="block text-sm font-semibold text-slate-700 mb-2">Эхлэх өдөр</label>
      <div class="relative max-w-xs">
        <input
          :value="form.startDate"
          type="date"
          class="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none focus:ring-2 focus:ring-teal-500/40 focus:border-teal-500"
          @input="updateField('startDate', ($event.target as HTMLInputElement).value)"
        />
        <Calendar class="w-4 h-4 text-slate-400 absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none" />
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-2">
      <div>
        <label class="block text-sm font-semibold text-slate-700 mb-2">Эхлэх цаг</label>
        <div class="relative">
          <select
            :value="form.startTime"
            class="w-full appearance-none rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none focus:ring-2 focus:ring-teal-500/40 focus:border-teal-500"
            @change="updateField('startTime', ($event.target as HTMLSelectElement).value)"
          >
            <option v-for="t in times" :key="t" :value="t">{{ t }}</option>
          </select>
          <ChevronDown class="w-4 h-4 text-slate-400 absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none" />
        </div>
      </div>
      <div>
        <label class="block text-sm font-semibold text-slate-700 mb-2">Дуусах цаг</label>
        <div class="relative">
          <select
            :value="form.endTime"
            class="w-full appearance-none rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none focus:ring-2 focus:ring-teal-500/40 focus:border-teal-500"
            @change="updateField('endTime', ($event.target as HTMLSelectElement).value)"
          >
            <option v-for="t in times" :key="t" :value="t">{{ t }}</option>
          </select>
          <ChevronDown class="w-4 h-4 text-slate-400 absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none" />
        </div>
      </div>
    </div>
    <p class="text-sm font-medium mb-5" :class="timeRangeInvalid ? 'text-red-500' : 'text-teal-700'">
      <template v-if="timeRangeInvalid">Дуусах цаг эхлэх цагаас хойш байх ёстой.</template>
      <template v-else>Та {{ requestedHours }} цагийн хүсэлт илгээх гэж байна.</template>
    </p>

    <div class="mb-5">
      <label class="block text-sm font-semibold text-slate-700 mb-2">Тайлбар</label>
      <textarea
        :value="form.description"
        rows="4"
        placeholder="Тайлбар оруулах"
        class="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none resize-y focus:ring-2 focus:ring-teal-500/40 focus:border-teal-500"
        @input="updateField('description', ($event.target as HTMLTextAreaElement).value)"
      />
    </div>

    <div class="mb-6">
      <label class="block text-sm font-semibold text-slate-700 mb-2">Багийн гишүүд</label>
      <div ref="teamWrapperRef" class="relative">
        <button
          type="button"
          class="w-full flex items-center justify-between rounded-xl border bg-white px-4 py-3 text-sm text-left outline-none focus:ring-2 focus:ring-teal-500/40 focus:border-teal-500"
          :class="[
            form.approverIds.length ? 'text-slate-700' : 'text-slate-400',
            approverError ? 'border-red-400' : 'border-slate-200',
          ]"
          @click.stop="teamOpen = !teamOpen"
        >
          <span class="truncate">{{ membersLabel }}</span>
          <ChevronDown
            class="w-4 h-4 text-slate-400 shrink-0 transition-transform"
            :class="{ 'rotate-180': teamOpen }"
          />
        </button>
        <div
          v-if="teamOpen"
          class="absolute z-10 mt-1 w-full rounded-xl border border-slate-200 bg-white shadow-lg max-h-56 overflow-auto py-1"
        >
          <label
            v-for="member in teamMembers"
            :key="member.id"
            class="flex items-center gap-3 px-4 py-2.5 text-sm text-slate-700 hover:bg-slate-50 cursor-pointer"
          >
            <input
              type="checkbox"
              class="rounded border-slate-300 text-teal-600 focus:ring-teal-500"
              :checked="form.approverIds.includes(member.id)"
              @change="toggleMember(member.id)"
            />
            {{ member.name }}
          </label>
        </div>
      </div>
      <p v-if="approverError" class="text-xs text-red-500 mt-1.5">Дор хаяж нэг багийн гишүүн сонгоно уу.</p>
    </div>
  </div>
</template>
