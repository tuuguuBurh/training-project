export default defineNuxtRouteMiddleware(() => {
  if (!useCookie('user-auth') || !useCookie('user-auth').value) {
    return navigateTo('/login')
  }
})
