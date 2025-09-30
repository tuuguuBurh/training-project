export const required = (v: any) => (v !== undefined && v !== '') || 'Утга оруулна уу.'

export const validateLogin = (inputString: string) => {
  const regex = /^[A-Za-z\d\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]{4,16}$/
  return regex.test(inputString) || 'please enter your login username in 4-16 characters.'
}

export const validatePassword = (inputString: string) => {
  const regex = /^[A-Za-z\d]{8,16}$/
  return regex.test(inputString) || 'Нууц үгийн урт 8-16 тэмдэгт байх ёстой.'
}

export const validateEmail = (v: any) => {
  if (typeof v === undefined || v === '' || v === null) {
    return true
  }
  const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  return pattern.test(v) || 'И-Мэйл буруу байна.'
}

export const validateRegister = (v: any) => {
  const regex = /^[А-Я|Ө|Ү]{2}\d{8}$/
  return regex.test(v) || 'Регистрийн дугаар буруу байна.'
}

export const validatePhoneNumber = (v: any) => {
  const regex = /^\d{8}$/
  return regex.test(v) || 'Утасны дугаар буруу байна.'
}

export const validateHeightWeight = (v: any) => {
  const regex = /^\d+(\.\d{1,2})?$/
  return regex.test(v) || 'Утга буруу байна.'
}

export const notMinusNumber = (v: any) => (v !== undefined && Number(v) >= 0) || `Сөрөг утга оруулах боломжгүй`

// XSS protection - sanitize user input
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

// Enhanced email validation with additional security checks
export const validateEmailSecure = (email: string): boolean | string => {
  if (!email) return 'Email is required'
  if (typeof email !== 'string') return 'Email must be a string'
  if (email.length > 254) return 'Email too long'
  if (email.length < 3) return 'Email too short'

  // Check for malicious patterns
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

// Secure password validation
export const validatePasswordSecure = (password: string): boolean | string => {
  if (!password) return 'Password is required'
  if (typeof password !== 'string') return 'Password must be a string'
  if (password.length < 8) return 'Password must be at least 8 characters'
  if (password.length > 128) return 'Password too long'

  return true
}
