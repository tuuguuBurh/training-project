<script setup lang="ts">
defineProps<{
  total: number
}>()
</script>

<template>
  <div class="border-b border-slate-200 bg-white">
    <div class="px-6 py-5 sm:px-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-slate-900">
            Чөлөөний хүсэлтүүд
            <span class="text-slate-400 font-medium">({{ total }})</span>
          </h1>
          <p class="mt-1 text-sm text-slate-500">Өнөөдөр болон сараар чөлөө авсан ажилчдын жагсаалт.</p>
        </div>
      </div>
    </div>
  </div>
</template>
