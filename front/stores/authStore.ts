import { defineStore } from 'pinia'
import { useAuth } from '~/composables/useAuth'
import { useCookieAuth } from '~/composables/useCookieAuth'
import type { LoginInput } from '~/types/auth'

interface AuthState {
  loading: boolean
  error: string | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    loading: false,
    error: null,
  }),

  getters: {
    userEmail(): string {
      const { userEmail } = useCookieAuth()
      return userEmail.value
    },

    isLoggedIn(): boolean {
      const { isAuthenticated } = useCookieAuth()
      return isAuthenticated.value
    },

    isLoading(): boolean {
      return this.loading
    },
  },

  actions: {
    async login(credentials: LoginInput): Promise<boolean> {
      this.loading = true
      this.error = null

      try {
        const { login } = useAuth()
        const response = await login(credentials)

        if (!response) {
          // Error is handled in useAuth via toast
          return false
        }

        const { setAuth } = useCookieAuth()
        setAuth(response.access_token, credentials.username)

        await navigateTo('/')
        return true
      } catch (error: any) {
        this.error = error.message || 'An unexpected error occurred'
        return false
      } finally {
        this.loading = false
      }
    },

    logout(): void {
      const { logout } = useAuth()
      logout()
    },

    clearError(): void {
      this.error = null
    },
  },
})
