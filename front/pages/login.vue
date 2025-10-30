<template>
  <div>
    <main>
      <section>
        <v-form v-model="isValid" fast-fail @submit.prevent="handleLogin">
          <div class="mb-3">
            <v-text-field
              v-model="credentials.username"
              :loading="isLoading"
              hide-details="auto"
              placeholder="Enter your email"
              :rules="[required, validateEmailSecure]"
              class="pb-8"
              variant="outlined"
              rounded="lg"
            />
            <v-text-field
              v-model="credentials.password"
              :loading="isLoading"
              hide-details="auto"
              placeholder="Enter your password"
              type="password"
              :rules="[required, validatePasswordSecure]"
              variant="outlined"
              rounded="lg"
            />
          </div>
          <div>
            <v-spacer />
            <button :disabled="isLoading || !isValid" type="submit">
              {{ isLoading ? 'Logging in...' : 'Login' }}
            </button>
          </div>
        </v-form>
      </section>
    </main>
  </div>
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
