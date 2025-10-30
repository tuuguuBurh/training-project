export const required = (v: any) => (v !== undefined && v !== '') || 'This field is required'

export const sanitizeInput = (value: string): string => {
  if (typeof value !== 'string') return ''
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;')
}

export const validateEmailSecure = (email: string): boolean | string => {
  if (!email) return 'Email is required'
  if (typeof email !== 'string') return 'Email must be a string'
  if (email.length > 254) return 'Email too long'
  if (email.length < 3) return 'Email too short'

  const maliciousPatterns = [/<script/i, /javascript:/i, /onclick=/i, /onerror=/i, /onload=/i]

  for (const pattern of maliciousPatterns) {
    if (pattern.test(email)) {
      return 'Invalid characters in email'
    }
  }

  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  if (!emailRegex.test(email)) return 'Valid email required'

  return true
}

export const validatePasswordSecure = (password: string): boolean | string => {
  if (!password) return 'Password is required'
  if (typeof password !== 'string') return 'Password must be a string'
  if (password.length < 8) return 'Password must be at least 8 characters'
  if (password.length > 128) return 'Password too long'

  return true
}

export const validateEmail = (v: any) => {
  if (typeof v === undefined || v === '' || v === null) {
    return true
  }
  const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  return pattern.test(v) || 'Invalid email format'
}

export const validatePassword = (inputString: string) => {
  const regex = /^[A-Za-z\d]{8,16}$/
  return regex.test(inputString) || 'Password must be 8-16 characters'
}

export const validatePhoneNumber = (v: any) => {
  const regex = /^\d{8}$/
  return regex.test(v) || 'Invalid phone number'
}

export const notMinusNumber = (v: any) => (v !== undefined && Number(v) >= 0) || 'Cannot be negative'
