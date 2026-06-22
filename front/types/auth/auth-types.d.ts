export interface LoginInput {
  email: string
  password: string
}

export interface AuthInput {
  access_token: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

export type PartialLoginInput = Partial<LoginInput>

declare global {
  interface LoginInput {
    email: string
    password: string
  }

  interface AuthInput {
    access_token: string
  }

  interface AuthResponse {
    access_token: string
    token_type: string
  }

  type PartialLoginInput = Partial<LoginInput>
}
