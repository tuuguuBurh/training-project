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
    LIST: '/leave-requests',
    MINE: '/leave-requests/mine',
    CREATE: '/leave-requests',
    TEAM_MEMBERS: '/leave-requests/team-members',
    MY_DECISION: (id: string) => `/leave-requests/${id}/my-decision`,
    STATUS: (id: string) => `/leave-requests/${id}/status`,
  },
  ADMIN: {
    DASHBOARD_STATS: '/admin/dashboard/stats',
    LEAVE_TYPES: '/admin/dashboard/leave-types',
    MONTHLY_TREND: '/admin/dashboard/monthly-trend',
    EMPLOYEES: '/admin/employees',
    LEAVE_REPORT: '/admin/reports/leaves',
  },
} as const

export const COOKIE_NAMES = {
  AUTH_TOKEN: 'user-auth',
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

export const balances = [
  { label: 'Ээлжийн амралт', value: 12 },
  { label: 'Өвчтэй', value: 5 },
  { label: 'Чөлөө', value: 3 },
]
