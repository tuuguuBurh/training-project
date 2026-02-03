<template>
  <v-container>
    <v-row justify="center" align="center" class="mt-10">
      <v-col cols="12" sm="8" md="6" class="text-center">
        <h1 class="text-h4 mb-4">Welcome</h1>
        <p class="text-subtitle-1 mb-6">
          Logged in as:
          <strong>{{ userEmail }}</strong>
        </p>

        <v-btn color="primary" prepend-icon="mdi-logout" variant="elevated" rounded="lg" @click="handleLogout">
          Logout
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
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
