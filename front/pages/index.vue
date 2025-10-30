<template>
  <div>
    <div class="user-info">
      <p>Welcome, {{ userEmail }}</p>
    </div>
    <button class="ml-5" @click="handleLogout">
      <v-icon>mdi-logout</v-icon>
      <span>Logout</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/authStore'

definePageMeta({
  layout: 'default',
  middleware: 'auth',
})

const authStore = useAuthStore()

const userEmail = computed(() => authStore.userEmail)

const handleLogout = () => {
  authStore.logout()
}
</script>

<style scoped>
.user-info {
  padding: 1rem;
}
</style>
