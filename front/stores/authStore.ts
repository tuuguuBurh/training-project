import { defineStore } from 'pinia'
import { useApiFetch } from '~/server/userApi'
import { type LoginInput, type AuthInput, type AuthResponse } from '~/types/auth'

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
      const email = useCookie('user-email')
      return email.value || ''
    },
    isLoggedIn(): boolean {
      const userAuthCookie = useCookie('user-auth')
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
        throw new Error(error.value?.data?.detail ?? '')
      } else {
        const auth = useCookie('user-auth')
        const authResponse = data as AuthResponse
        const authData: AuthInput = {
          access_token: authResponse.access_token,
        }

        auth.value = authData

        const email = useCookie('user-email')
        email.value = user.username
        navigateTo('/')
      }
    },
    logout() {
      const auth = useCookie('user-auth')
      auth.value = undefined
      const email = useCookie('user-email')
      email.value = undefined
      useNuxtApp().$toast.success('Амжилттай гарлаа.')
      navigateTo('/login')
    },
  },
})
