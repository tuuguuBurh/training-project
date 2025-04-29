import { navigateTo, useCookie, useRuntimeConfig } from 'nuxt/app'
import { type AuthInput } from '~/types/auth'
import { $fetch, type FetchOptions } from 'ofetch'

export const useApiFetch = async <T>(path: string, options: FetchOptions<'json'> = {}, isFormData = false) => {
  const config = useRuntimeConfig()
  const userAuthData = useCookie('user-auth').value as AuthInput | null

  const headers: any = {}

  if (isFormData) {
    // Let browser set Content-Type for FormData
  } else {
    headers['Content-Type'] = 'application/json'
  }

  if (userAuthData) {
    headers.Authorization = `Bearer ${userAuthData.access_token}`
  }

  try {
    const data = await $fetch<T>(config.public.apiBase + path, {
      ...options,
      headers: {
        ...headers,
        ...(options.headers || {}),
      },
    })
    return { data, error: { value: null } }
  } catch (error: any) {
    // Handle auth errors
    if (error?.status === 401) {
      const auth = useCookie('user-auth')
      auth.value = undefined
      navigateTo('/login')
      throw new Error('Unauthorized')
    }
    if (error?.status === 403) {
      navigateTo('/403')
      throw new Error('Forbidden')
    }
    return { data: null, error: { value: error } }
  }
}
