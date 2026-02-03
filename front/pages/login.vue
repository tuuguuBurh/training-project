<template>
  <v-container fill-height class="d-flex align-center justify-center" style="min-height: 80vh">
    <v-card width="100%" max-width="400" elevation="2" rounded="xl" class="pa-6">
      <v-card-title class="text-h5 text-center mb-4">Login</v-card-title>

      <v-card-text>
        <v-form v-model="isValid" fast-fail @submit.prevent="handleLogin">
          <v-text-field
            v-model="credentials.username"
            :loading="isLoading"
            label="Email"
            placeholder="Enter your email"
            :rules="[required, validateEmailSecure]"
            variant="outlined"
            rounded="lg"
            class="mb-4"
          />

          <v-text-field
            v-model="credentials.password"
            :loading="isLoading"
            label="Password"
            placeholder="Enter your password"
            type="password"
            :rules="[required, validatePasswordSecure]"
            variant="outlined"
            rounded="lg"
            class="mb-6"
          />

          <v-btn
            :disabled="isLoading || !isValid"
            :loading="isLoading"
            type="submit"
            color="primary"
            block
            size="large"
            variant="elevated"
            rounded="lg"
          >
            Login
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script lang="ts" setup>
import { required, validateEmailSecure, validatePasswordSecure } from '@/utils/validates'
import { useAuthStore } from '~/stores/authStore'
import type { LoginInput } from '~/types/auth'

definePageMeta({
  layout: 'login',
})

const authStore = useAuthStore()
const toast = useNuxtApp().$toast

const isLoading = ref(false)
const isValid = ref(false)
const credentials = ref<LoginInput>({ username: '', password: '' })

const handleLogin = async () => {
  if (!isValid.value) return

  isLoading.value = true
  try {
    const success = await authStore.login(credentials.value)
    if (success) {
      toast.success('Successfully logged in')
    }
  } catch (error: any) {
    toast.error(error.message || 'Login failed')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped></style>
