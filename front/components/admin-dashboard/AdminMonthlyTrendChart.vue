<script setup lang="ts">
import { BarElement, CategoryScale, Chart as ChartJS, Legend, LinearScale, Title, Tooltip } from 'chart.js'
import { Bar } from 'vue-chartjs'
import type { MonthlyTrendItem } from '~/types/admin/admin-types'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const props = defineProps<{
  items: MonthlyTrendItem[]
  loading: boolean
}>()

const chartData = computed(() => ({
  labels: props.items.map((item) => item.label),
  datasets: [
    {
      label: 'Хүсэлтийн тоо',
      data: props.items.map((item) => item.count),
      backgroundColor: '#1877F2',
      borderRadius: 6,
      maxBarThickness: 40,
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        precision: 0,
      },
      grid: {
        color: '#f1f5f9',
      },
    },
    x: {
      grid: {
        display: false,
      },
    },
  },
}
</script>

<template>
  <div class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
    <h3 class="mb-4 text-lg font-semibold text-slate-900">Сарын чөлөөний хүсэлт</h3>

    <div v-if="loading" class="flex h-72 items-center justify-center">
      <i class="pi pi-spin pi-spinner text-2xl text-blue-500" />
    </div>

    <div v-else-if="items.length === 0" class="flex h-72 items-center justify-center text-sm text-slate-500">
      Мэдээлэл байхгүй
    </div>

    <div v-else class="h-72">
      <Bar :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>
