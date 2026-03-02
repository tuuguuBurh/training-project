export interface LoginInput {
  username: string
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
  type LoginInput = {
    username: string
    password: string
  }

  type AuthInput = {
    access_token: string
  }

  type AuthResponse = {
    access_token: string
    token_type: string
  }

  type PartialLoginInput = Partial<LoginInput>
}
