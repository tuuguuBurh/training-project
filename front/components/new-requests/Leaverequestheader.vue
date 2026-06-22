<script setup lang="ts">
import { ref } from 'vue'
import { Info, ChevronDown } from 'lucide-vue-next'

interface BalanceItem {
  label: string
  value: number
}

defineProps<{
  balances?: BalanceItem[]
}>()

const balanceOpen = ref(false)
</script>

<template>
  <div>
    <button
      type="button"
      class="w-full cursor-pointer flex items-center justify-between gap-3 border border-slate-200 rounded-xl px-4 py-4 mb-6 hover:bg-slate-50 transition-colors"
      @click="balanceOpen = !balanceOpen"
    >
      <span class="flex items-center gap-3 text-slate-700 font-semibold">
        <Info class="w-5 h-5 text-slate-400" />
        Чөлөөний үлдэгдэл
      </span>
      <ChevronDown class="w-5 h-5 text-slate-400 transition-transform" :class="{ 'rotate-180': balanceOpen }" />
    </button>

    <div v-if="balanceOpen && balances?.length" class="-mt-3 mb-6 grid grid-cols-3 gap-3 text-center">
      <div v-for="b in balances" :key="b.label" class="rounded-lg bg-slate-50 border border-slate-200 p-3">
        <p class="text-2xl font-bold text-teal-700">{{ b.value }}</p>
        <p class="text-xs text-slate-500 mt-1">{{ b.label }}</p>
      </div>
    </div>
  </div>
</template>
