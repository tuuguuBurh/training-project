// https://v3.nuxtjs.org/api/configuration/nuxt.config
// @ts-nocheck

export default defineNuxtConfig({
  devtools: { enabled: true },
  head: {
    title: 'Front',
    htmlAttrs: {
      lang: 'en',
    },
    meta: [
      { charset: 'utf-8' },
      {
        name: 'viewport',
        content: 'width=device-width, initial-scale=1',
      },
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon/favicon.ico' },
      {
        rel: 'apple-touch-icon',
        sizes: '180x180',
        href: '/favicon/apple-touch-icon.png',
      },
      {
        rel: 'icon',
        type: 'image/png',
        sizes: '32x32',
        href: '/favicon/favicon-32x32.png',
      },
      {
        rel: 'icon',
        type: 'image/png',
        sizes: '16x16',
        href: '/favicon/favicon-16x16.png',
      },
      {
        rel: 'icon',
        type: 'image/png',
        sizes: '192x192',
        href: '/favicon/android-chrome-192x192.png',
      },
      { rel: 'manifest', href: '/favicon/site.webmanifest' },
      {
        rel: 'stylesheet',
        href: 'https://cdn.jsdelivr.net/npm/@mdi/font@6.5.95/css/materialdesignicons.min.css',
        integrity: 'sha384-scpQJqXbp/4O66QYGm9hiZWcHYBwPwFE/4BPPc63T0ziKqrQVOIwWnSsEIjNuH3e',
        crossorigin: 'anonymous',
      },
      {
        rel: 'preconnect',
        href: 'https://fonts.googleapis.com',
        crossorigin: 'anonymous',
      },
      {
        rel: 'preconnect',
        href: 'https://fonts.gstatic.com',
        crossorigin: 'anonymous',
      },
      {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css2?family=Mulish:wght@400;700&display=swap',
      },
    ],
  },
  components: true,
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api/v1',
    },
  },
  modules: ['@pinia/nuxt', '@nuxt/icon', '@nuxtjs/robots'],
  pinia: {
    storesDirs: ['./stores/**'],
    autoImports: ['defineStore', ['defineStore', 'definePiniaStore']],
  },
  robots: {
    UserAgent: '*',
    Disallow: ['/api/', '/.nuxt/', '/admin/'],
    Allow: '/',
  },
  css: ['vuetify/lib/styles/main.sass', '@/assets/settings.scss', '@/assets/main.scss'],
  build: {
    transpile: ['vuetify'],
  },
  vite: {
    define: {
      'process.env.DEBUG': false,
    },
    ssr: {
      noExternal: ['vuetify'],
    },
  },
  nitro: {
    routeRules: {
      '/**': {
        headers: {
          'Content-Security-Policy': [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline'" + (process.env.NODE_ENV === 'development' ? " 'unsafe-eval'" : ''), // unsafe-eval only in development
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net",
            "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net",
            "img-src 'self' data: https:",
            "connect-src 'self' " +
              new URL(process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api/v1').origin +
              ' ws: wss:',
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'",
          ].join('; '),
          'X-Frame-Options': 'DENY',
          'X-Content-Type-Options': 'nosniff',
          'Referrer-Policy': 'strict-origin-when-cross-origin',
          'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
          'X-XSS-Protection': '1; mode=block',
        },
      },
    },
  },
})
