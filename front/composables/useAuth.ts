import { useApi } from './useApi'
import { API_ENDPOINTS } from '~/constants'
import type { LoginInput, AuthResponse } from '~/types/auth'

export const useAuth = () => {
  const api = useApi()
  const router = useRouter()
  const toast = useNuxtApp().$toast

  const login = async (credentials: LoginInput): Promise<AuthResponse | null> => {
    const formData = new URLSearchParams()
    formData.append('grant_type', 'password')
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)

    const { data, error } = await api.post<AuthResponse>(API_ENDPOINTS.AUTH.LOGIN, formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })

    if (error) {
      toast.error(error.message)
      return null
    }

    return data
  }

  const logout = () => {
    const cookieAuth = useCookieAuth()
    cookieAuth.clearAuth()
    toast.success('Successfully logged out')
    router.push('/login')
  }

  return {
    login,
    logout,
  }
}
