import { getAuthCookie } from '~/utils/cookieConfig'

export default defineNuxtRouteMiddleware(() => {
  const userAuth = getAuthCookie()

  if (!userAuth || !userAuth.value) {
    return navigateTo('/login')
  }
})
