<script setup lang="ts">
defineProps<{
  submitted: boolean
  disabled?: boolean
  loading?: boolean
}>()
</script>

<template>
  <div>
    <button
      type="submit"
      class="rounded-lg bg-[#1877F2] px-6 py-2.5 text-sm font-semibold text-white hover:bg-[#1877F2] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      :disabled="disabled"
    >
      {{ loading ? 'Илгээж байна...' : 'Илгээх' }}
    </button>

    <p v-if="submitted" class="mt-4 text-sm font-medium text-[#1877F2]">Таны хүсэлт амжилттай илгээгдлээ.</p>
  </div>
</template>
