<script setup lang="ts">
import type { DashboardStats } from '~/types/admin/admin-types'

defineProps<{
  stats: DashboardStats | null
  loading: boolean
}>()

const cards = [
  { key: 'total_users', label: 'Нийт ажилтан', icon: 'pi pi-users', color: 'text-blue-600 bg-blue-50' },
  { key: 'total_requests', label: 'Нийт хүсэлт', icon: 'pi pi-inbox', color: 'text-slate-600 bg-slate-50' },
  { key: 'pending_requests', label: 'Хүлээгдэж буй', icon: 'pi pi-clock', color: 'text-amber-600 bg-amber-50' },
  {
    key: 'approved_requests',
    label: 'Зөвшөөрсөн',
    icon: 'pi pi-check-circle',
    color: 'text-emerald-600 bg-emerald-50',
  },
  { key: 'rejected_requests', label: 'Татгалзсан', icon: 'pi pi-times-circle', color: 'text-rose-600 bg-rose-50' },
  { key: 'total_leave_days', label: 'Ашигласан өдөр', icon: 'pi pi-calendar', color: 'text-indigo-600 bg-indigo-50' },
] as const
</script>

<template>
  <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-6">
    <template v-if="loading">
      <div v-for="card in cards" :key="card.key" class="animate-pulse rounded-xl border border-slate-200 bg-white p-5">
        <div class="mb-3 h-10 w-10 rounded-lg bg-slate-100" />
        <div class="mb-2 h-7 w-16 rounded bg-slate-100" />
        <div class="h-4 w-24 rounded bg-slate-100" />
      </div>
    </template>

    <template v-else>
      <div
        v-for="card in cards"
        :key="card.key"
        class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition-shadow hover:shadow-md"
      >
        <div class="mb-3 flex items-center justify-between">
          <div class="flex h-10 w-10 items-center justify-center rounded-lg" :class="card.color">
            <i :class="card.icon" />
          </div>
        </div>
        <p class="text-2xl font-bold text-slate-900">
          {{ stats ? stats[card.key] : 0 }}
        </p>
        <p class="mt-1 text-sm text-slate-500">{{ card.label }}</p>
      </div>
    </template>
  </div>
</template>
