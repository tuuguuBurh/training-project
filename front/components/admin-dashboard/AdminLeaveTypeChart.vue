<script setup lang="ts">
import { ArcElement, Chart as ChartJS, Legend, Tooltip } from 'chart.js'
import { Doughnut } from 'vue-chartjs'
import type { LeaveTypeStat } from '~/types/admin/admin-types'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps<{
  items: LeaveTypeStat[]
  loading: boolean
}>()

const chartColors = ['#1877F2', '#10B981', '#F59E0B', '#8B5CF6', '#EF4444', '#06B6D4', '#64748B']

const chartData = computed(() => ({
  labels: props.items.map((item) => item.name),
  datasets: [
    {
      data: props.items.map((item) => item.count),
      backgroundColor: props.items.map((_, index) => chartColors[index % chartColors.length]),
      borderWidth: 2,
      borderColor: '#ffffff',
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: {
        boxWidth: 12,
        padding: 16,
      },
    },
  },
}
</script>

<template>
  <div class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
    <h3 class="mb-4 text-lg font-semibold text-slate-900">Чөлөөний төрлийн статистик</h3>

    <div v-if="loading" class="flex h-72 items-center justify-center">
      <i class="pi pi-spin pi-spinner text-2xl text-blue-500" />
    </div>

    <div v-else-if="items.length === 0" class="flex h-72 items-center justify-center text-sm text-slate-500">
      Мэдээлэл байхгүй
    </div>

    <div v-else class="h-72">
      <Doughnut :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>
