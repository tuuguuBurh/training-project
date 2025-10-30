import { useCookieAuth } from '~/composables/useCookieAuth'
import { ROUTES } from '~/constants'

export default defineNuxtRouteMiddleware(() => {
  const { isAuthenticated } = useCookieAuth()

  if (!isAuthenticated.value) {
    return navigateTo(ROUTES.LOGIN)
  }
})
