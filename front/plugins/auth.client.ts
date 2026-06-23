export default defineNuxtPlugin(async () => {
  const auth = useAuth()

  if (auth.checkAuthStatus() && !auth.user.value) {
    await auth.fetchMe()
  }
})
