<template>
  <div class="info-panel">
    <div class="text-center pa-8">
      <v-icon size="64" color="warning" class="mb-4">mdi-alert-circle-outline</v-icon>
      <h2 class="text-h4 mb-2">{{ title }}</h2>
      <p class="text-body-1 text-medium-emphasis">{{ message }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string
  message: string
  altText?: string
}

const props = withDefaults(defineProps<Props>(), {
  altText: 'Information',
})
</script>

<style scoped>
.info-panel {
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
