import { navigateTo } from 'nuxt/app'
import type { FetchOptions } from 'ofetch'
import { getAuthCookie } from '~/utils/cookieConfig'
import { ApiError, AuthError, NetworkError } from '~/utils/errors'
import { HTTP_STATUS, ROUTES } from '~/constants'

export interface ApiResponse<T> {
  data: T | null
  error: ApiError | AuthError | NetworkError | null
}

export const useApi = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase

  const apiFetch = async <T>(path: string, options: FetchOptions<'json'> = {}): Promise<ApiResponse<T>> => {
    const authCookie = getAuthCookie()
    const headers: Record<string, string> = {
      ...((options.headers as Record<string, string>) || {}),
    }

    if (authCookie.value) {
      headers.Authorization = `Bearer ${authCookie.value}`
    }

    // Set JSON content type if body is present and not FormData
    if (options.body && !(options.body instanceof FormData) && !headers['Content-Type']) {
      headers['Content-Type'] = 'application/json'
    }

    try {
      const data = (await $fetch<T>(`${baseURL}${path}`, {
        ...options,
        headers,
      } as any)) as T

      return { data, error: null }
    } catch (error: any) {
      return handleApiError(error)
    }
  }

  const handleApiError = <T>(error: any): ApiResponse<T> => {
    const statusCode = error?.status || error?.statusCode

    if (statusCode === HTTP_STATUS.UNAUTHORIZED) {
      const auth = getAuthCookie()
      auth.value = null
      navigateTo(ROUTES.LOGIN)
      return {
        data: null,
        error: new AuthError('Session expired. Please login again.'),
      }
    }

    if (statusCode === HTTP_STATUS.FORBIDDEN) {
      navigateTo(ROUTES.FORBIDDEN)
      return {
        data: null,
        error: new ApiError('Access denied', HTTP_STATUS.FORBIDDEN),
      }
    }

    // Check for network connectivity in a way that works during SSR
    if (import.meta.client && !navigator.onLine) {
      return {
        data: null,
        error: new NetworkError('No internet connection'),
      }
    }

    const message = error?.data?.detail || error?.message || 'An error occurred'
    return {
      data: null,
      error: new ApiError(message, statusCode, error?.data),
    }
  }

  return {
    get: <T>(path: string, options?: FetchOptions<'json'>) => apiFetch<T>(path, { ...options, method: 'GET' }),

    post: <T>(path: string, body?: any, options?: FetchOptions<'json'>) =>
      apiFetch<T>(path, { ...options, method: 'POST', body }),

    put: <T>(path: string, body?: any, options?: FetchOptions<'json'>) =>
      apiFetch<T>(path, { ...options, method: 'PUT', body }),

    delete: <T>(path: string, options?: FetchOptions<'json'>) => apiFetch<T>(path, { ...options, method: 'DELETE' }),

    patch: <T>(path: string, body?: any, options?: FetchOptions<'json'>) =>
      apiFetch<T>(path, { ...options, method: 'PATCH', body }),
  }
}
