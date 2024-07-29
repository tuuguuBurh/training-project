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
