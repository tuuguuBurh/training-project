export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    ME: '/auth/me',
    LOGOUT: '/auth/logout',
  },
  USERS: {
    LIST: '/users',
    CREATE: '/users',
    UPDATE: (id: string) => `/users/${id}`,
    DELETE: (id: string) => `/users/${id}`,
    GET: (id: string) => `/users/${id}`,
  },
  LEAVE_TYPES: {
    LIST: '/leave-types',
  },
  LEAVE_REQUESTS: {
    CREATE: '/leave-requests',
    TEAM_MEMBERS: '/leave-requests/team-members',
  },
} as const

export const COOKIE_NAMES = {
  AUTH_TOKEN: 'user-auth',
  USER_EMAIL: 'user-email',
} as const

export const HTTP_STATUS = {
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  INTERNAL_SERVER_ERROR: 500,
} as const

export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  FORBIDDEN: '/403',
} as const
