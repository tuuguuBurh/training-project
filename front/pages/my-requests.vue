<script setup lang="ts">
import MyRequestBalance from '~/components/my-requests/MyRequestBalance.vue'
import MyRequestHeader from '~/components/my-requests/MyRequestHeader.vue'
import MyRequestHistory from '~/components/my-requests/MyRequestHistory.vue'
</script>

<template>
  <div class="p-4">
    <MyRequestHeader />
    <MyRequestBalance />
    <MyRequestHistory />
  </div>
</template>
