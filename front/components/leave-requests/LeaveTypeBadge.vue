<script setup lang="ts">
defineProps<{
  name: string
}>()

const palette = [
  'bg-blue-50 text-blue-700',
  'bg-sky-50 text-sky-700',
  'bg-violet-50 text-violet-700',
  'bg-slate-100 text-slate-600',
  'bg-orange-50 text-orange-700',
  'bg-emerald-50 text-emerald-700',
]

function styleFor(name: string) {
  let hash = 0
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash)
  }
  return palette[Math.abs(hash) % palette.length]
}
</script>

<template>
  <span class="inline-flex items-center rounded-md px-2 py-0.5 text-xs font-medium capitalize" :class="styleFor(name)">
    {{ name }}
  </span>
</template>
