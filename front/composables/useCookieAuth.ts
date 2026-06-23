import { getAuthCookie } from '~/utils/cookieConfig'
import { COOKIE_NAMES } from '~/constants'

export const useCookieAuth = () => {
  const authCookie = getAuthCookie(COOKIE_NAMES.AUTH_TOKEN)
  const isAuthenticated = computed(() => !!authCookie.value)

  const setAuth = (token: string) => {
    authCookie.value = token
  }

  const clearAuth = () => {
    authCookie.value = null
  }

  return {
    isAuthenticated,
    setAuth,
    clearAuth,
    authToken: computed(() => authCookie.value),
  }
}
