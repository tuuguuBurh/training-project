<template>
  <div>
    <main>
      <section>
        <v-form v-model="valid" fast-fail @submit.prevent.stop="login">
          <div class="mb-3">
            <v-text-field
              v-model="user.username"
              :loading="isLoading"
              hide-details="auto"
              placeholder="Бүртгэлтэй имэйлээ оруулна уу"
              :rules="[required, validateEmailSecure]"
              class="pb-8"
              variant="outlined"
              rounded="lg"
            />
            <v-text-field
              v-model="user.password"
              :loading="isLoading"
              hide-details="auto"
              :placeholder="'Нууц үг'"
              type="password"
              :rules="[required, validatePasswordSecure]"
              variant="outlined"
              rounded="lg"
            />
          </div>
          <div>
            <v-spacer />
            <button :loading="isLoading" type="submit">Нэвтрэх</button>
          </div>
        </v-form>
      </section>
    </main>
  </div>
</template>

<script lang="ts" setup>
import { required, validateEmailSecure, validatePasswordSecure } from '@/utils/validates'
import { userAuthStore } from '~/stores/authStore'
import { type LoginInput } from '~/types/auth'

definePageMeta({
  layout: 'login',
})

const authStore = userAuthStore()

const isLoading = ref<boolean>(false)
const valid = ref(false)

const user = ref<LoginInput>({ username: '', password: '' })

const login = async () => {
  try {
    if (valid.value) {
      isLoading.value = true
      await authStore.login(user.value)
      useNuxtApp().$toast.success('Амжилттай нэвтэрлээ')
    }
  } catch (error: any) {
    useNuxtApp().$toast.error(error.message)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped></style>
