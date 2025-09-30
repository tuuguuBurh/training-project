import { defineStore } from 'pinia'
import { useApiFetch } from '~/server/userApi'
import { type LoginInput, type AuthInput, type AuthResponse } from '~/types/auth'
import { getAuthCookie, getEmailCookie } from '~/utils/cookieConfig'

interface IStateStore {
  loading: boolean
  errors: string[]
}

export const userAuthStore = defineStore('userAuthStore', {
  state: (): IStateStore => ({
    loading: false,
    errors: [],
  }),
  getters: {
    userEmail(): string {
      const email = getEmailCookie()
      return email.value || ''
    },
    isLoggedIn(): boolean {
      const userAuthCookie = getAuthCookie()
      return !!userAuthCookie.value
    },
  },
  actions: {
    async login(user: LoginInput) {
      const formData = new URLSearchParams()
      formData.append('grant_type', 'password')
      formData.append('username', user.username)
      formData.append('password', user.password)

      const { data, error } = await useApiFetch('/auth/login', {
        method: 'post',
        body: formData,
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      })
      if (error.value) {
        throw new Error(error.value?.message ?? 'Login failed')
      } else {
        const auth = getAuthCookie()
        const authResponse = data as AuthResponse

        auth.value = authResponse.access_token

        const email = getEmailCookie()
        email.value = user.username
        navigateTo('/')
      }
    },
    logout() {
      const auth = getAuthCookie()
      auth.value = undefined
      const email = getEmailCookie()
      email.value = undefined
      useNuxtApp().$toast.success('Амжилттай гарлаа.')
      navigateTo('/login')
    },
  },
})
