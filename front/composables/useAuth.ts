import { useApi } from './useApi'
import { API_ENDPOINTS } from '~/constants'
import type { LoginInput, AuthResponse, User } from '~/types/auth/auth-types'

export const useAuth = () => {
  const api = useApi()
  const router = useRouter()
  const toast = useNuxtApp().$toast
  const cookieAuth = useCookieAuth()

  const loading = ref(false)
  const error = ref<string[]>([])
  const user = useState<User | null>('auth-user', () => null)

  const isLoggedIn = computed(() => cookieAuth.isAuthenticated.value)
  const access_token = computed(() => cookieAuth.authToken.value || '')

  const fetchMe = async (token?: string): Promise<User | null> => {
    const authToken = token || cookieAuth.authToken.value
    if (!authToken) {
      user.value = null
      return null
    }

    const { data, error: apiError } = await api.get<User>(API_ENDPOINTS.AUTH.ME, {
      headers: { Authorization: `Bearer ${authToken}` },
    })

    if (apiError || !data) {
      cookieAuth.clearAuth()
      user.value = null
      return null
    }

    user.value = data
    return data
  }

  const login = async (credentials: LoginInput): Promise<boolean> => {
    loading.value = true
    error.value = []

    try {
      const formData = new URLSearchParams()
      formData.append('grant_type', 'password')
      formData.append('username', credentials.email.trim().toLowerCase())
      formData.append('password', credentials.password)

      const { data, error: apiError } = await api.post<AuthResponse>(API_ENDPOINTS.AUTH.LOGIN, formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      })

      if (apiError) {
        error.value = [apiError.message]
        toast.error(apiError.message)
        return false
      }

      if (data) {
        cookieAuth.setAuth(data.access_token)
        await fetchMe(data.access_token)

        toast.success('Login successful')
        await router.push('/')
        return true
      }

      return false
    } catch (err: any) {
      let errorMessage = 'Login failed'

      if (err.status === 401) {
        errorMessage = 'Invalid email or password'
      } else if (err.status === 403) {
        errorMessage = 'Account is disabled or suspended'
      } else if (err.status >= 500) {
        errorMessage = 'Server error. Please try again later'
      } else if (err.message) {
        errorMessage = err.message
      }

      error.value = [errorMessage]
      toast.error(errorMessage)
      return false
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    cookieAuth.clearAuth()
    user.value = null
    error.value = []
    toast.success('Successfully logged out')
    router.push('/login')
  }

  const checkAuthStatus = (): boolean => {
    return cookieAuth.isAuthenticated.value
  }

  return {
    loading: readonly(loading),
    error: readonly(error),
    user: readonly(user),
    isLoggedIn,
    access_token,
    login,
    logout,
    fetchMe,
    checkAuthStatus,
  }
}
