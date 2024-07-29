export type LoginInput = {
  username: string
  password: string
}

export type AuthInput = {
  access_token: string
}

export type AuthResponse = {
  access_token: string
  token_type: string
}
