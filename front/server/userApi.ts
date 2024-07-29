import { navigateTo, useCookie, useFetch, type UseFetchOptions } from 'nuxt/app'
import { type AuthInput } from '~/types/AuthTypes'

export const useApiFetch = async <T>(path: string, options: UseFetchOptions<T> = {}, isFormData = false) => {
  const config = useRuntimeConfig()
  const userAuthData = useCookie('user-auth').value as AuthInput | null

  const headers: any = {}

  if (isFormData) {
    // headers['Content-Type'] = 'multipart/form-data';
  } else {
    headers['Content-Type'] = 'application/json'
  }

  if (userAuthData) {
    headers.Authorization = `Bearer ${userAuthData.access_token}`
  }

  const response = await useFetch(config.public.apiBase + path, {
    immediate: false,
    server: false,
    ...options,
    headers: {
      ...headers,
      ...options.headers,
    },
  })

  await response.execute()

  if (response.error.value) {
    // eslint-disable-next-line no-console
    console.log('Fetch error:', response.error.value)
  }

  if (response && response.error.value?.statusCode === 401) {
    const auth = useCookie('user-auth')
    auth.value = undefined
    navigateTo('/login')
    throw new Error('Unauthorized')
  }

  return response
}
