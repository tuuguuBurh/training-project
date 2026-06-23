export default defineNuxtRouteMiddleware(async () => {
  const { user, fetchMe, checkAuthStatus } = useAuth()

  if (checkAuthStatus() && !user.value) {
    await fetchMe()
  }

  if (user.value?.role !== 'ADMIN') {
    return navigateTo('/403')
  }
})
