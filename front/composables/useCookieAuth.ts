import { getAuthCookie, getEmailCookie } from '~/utils/cookieConfig'
import { COOKIE_NAMES } from '~/constants'

export const useCookieAuth = () => {
  const authCookie = getAuthCookie(COOKIE_NAMES.AUTH_TOKEN)
  const emailCookie = getEmailCookie(COOKIE_NAMES.USER_EMAIL)

  const isAuthenticated = computed(() => !!authCookie.value)
  const userEmail = computed(() => emailCookie.value || '')

  const setAuth = (token: string, email: string) => {
    authCookie.value = token
    emailCookie.value = email
  }

  const clearAuth = () => {
    authCookie.value = null
    emailCookie.value = null
  }

  return {
    isAuthenticated,
    userEmail,
    setAuth,
    clearAuth,
    authToken: computed(() => authCookie.value),
  }
}
