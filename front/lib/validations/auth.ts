import { z } from 'zod'
import { commonValidations } from '~/utils/validates'

export const loginSchema = z.object({
  email: commonValidations.email,
  password: commonValidations.password,
})

export const loginFormSchema = loginSchema.extend({
  remember: z.boolean().optional().default(false),
})

export type LoginInput = z.infer<typeof loginSchema>
export type LoginFormInput = z.infer<typeof loginFormSchema>

export const validateEmail = (email: string): string | undefined => {
  const result = commonValidations.email.safeParse(email)
  return result.success ? undefined : result.error.issues[0]?.message
}

export const validatePassword = (password: string): string | undefined => {
  const result = commonValidations.password.safeParse(password)
  return result.success ? undefined : result.error.issues[0]?.message
}
