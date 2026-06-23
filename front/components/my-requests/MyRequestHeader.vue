<script setup lang="ts">
import { ChevronLeft } from 'lucide-vue-next'

const router = useRouter()

const goBack = () => {
  router.push('/new-request')
}
</script>

<template>
  <div class="flex justify-between items-center p-4">
    <div>
      <h1 class="text-xl font-bold text-slate-900">Чөлөөний үлдэгдэл</h1>
    </div>
    <div
      class="inline-flex py-2 px-4 m-3 gap-2 items-center border cursor-pointer rounded-lg border-slate-200 bg-[#4294ff] text-white"
      @click="goBack"
    >
      <ChevronLeft class="w-5 h-5" />
      <button class="text-l font-medium text-white cursor-pointer">Хүсэлт илгээх</button>
    </div>
  </div>
</template>
