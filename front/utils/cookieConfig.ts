/**
 * Shared cookie configuration for the application
 * Ensures consistent security settings across all cookie usage
 */

import { useCookie } from 'nuxt/app'

export interface CookieConfig {
  secure: boolean
  httpOnly: boolean
  sameSite: 'strict' | 'lax' | 'none'
  maxAge: number
}

/**
 * Standard secure cookie configuration
 * - secure: true in production (HTTPS only)
 * - httpOnly: false (allows client-side access for auth tokens)
 * - sameSite: 'strict' (CSRF protection)
 * - maxAge: 8 hours (28800 seconds)
 */
export const SECURE_COOKIE_CONFIG: CookieConfig = {
  secure: process.env.NODE_ENV === 'production',
  httpOnly: false,
  sameSite: 'strict',
  maxAge: 60 * 60 * 8, // 8 hours
}

/**
 * Convenience function to get auth cookie with secure config
 */
export const getAuthCookie = (name: string = 'user-auth') => {
  return useCookie(name, SECURE_COOKIE_CONFIG)
}

/**
 * Convenience function to get email cookie with secure config
 */
export const getEmailCookie = (name: string = 'user-email') => {
  return useCookie(name, SECURE_COOKIE_CONFIG)
}
