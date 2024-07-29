<template>
  <div>{{ email }}</div>
  <button class="ml-5" @click="logout">
    <v-icon>mdi-logout</v-icon>
    <span>Гарах</span>
  </button>
</template>

<script setup lang="ts">
import { userAuthStore } from '@/store/authStore'

const authStore = userAuthStore()

definePageMeta({
  layout: 'default',
  middleware: 'auth',
})

const email = computed(() => String(authStore.userEmail))

const logout = () => {
  authStore.logout()
}
</script>
<style scoped></style>
