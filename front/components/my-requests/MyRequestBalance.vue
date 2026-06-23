<script setup lang="ts">
import { balances } from '~/constants'
</script>
<template>
  <div class="-mt-3 mb-6 grid grid-cols-3 gap-3 text-center">
    <div v-for="b in balances" :key="b.label" class="rounded-lg bg-white border border-slate-200 p-3">
      <p class="text-2xl font-bold text-[#1877F2]">{{ b.value }}</p>
      <p class="text-l text-slate-500 mt-1">{{ b.label }}</p>
    </div>
  </div>
</template>
