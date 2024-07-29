// plugins/vuetify.js
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'

export default defineNuxtPlugin((nuxtApp) => {
  const vuetify = createVuetify({
    ssr: true,
    icons: {
      defaultSet: 'mdi',
      aliases,
      sets: {
        mdi,
      },
    },
    theme: {
      defaultTheme: 'light',
      themes: {
        dark: {
          colors: {
            primary: '#001C89',
            secondary: '#292524',
            info: '#1c92f2',
            success: '#1c9b1c',
            warning: '#cccc14',
            error: '#da2f2f',
            midnightblue: '#000E59',
            onyxblack: '3B7DFC',
            darkblue: '#00072B',
            bgwhite: '#E6E6E6',
            green: '#7ccbaf',
            lightgreen: '#EDF5E9',
          },
        },
        light: {
          dark: false,
          colors: {
            primary: '#001C89',
            secondary: '#EEEEEE',
            info: '#1c92f2',
            success: '#bef264',
            warning: '#fcd34d',
            error: '#ef4444',
            midnightblue: '#000E59',
            onyxblack: '3B7DFC',
            darkblue: '#00072B',
            bgwhite: '#E6E6E6',
            green: '#7ccbaf',
            lightgreen: '#EDF5E9',
          },
        },
      },
    },
    components,
    directives,
    defaults: {
      global: {
        ripple: false,
      },
    },
  })

  nuxtApp.vueApp.use(vuetify)
})
