/**
 * 用户相关类型定义
 */

export type UserRole = 'user' | 'merchant' | 'organizer' | 'admin'
export type UserStatus = 'active' | 'banned' | 'inactive'

export interface User {
  id: number
  platform_id: string
  nickname: string
  avatar_url?: string
  phone?: string
  industry?: string
  role: UserRole
  status: UserStatus
  created_at: string
  updated_at: string
}

export interface EloScore {
  id: number
  user_id: number
  score: number
  tier: 'bronze' | 'silver' | 'gold' | 'platinum' | 'diamond'
  total_matches: number
  wins: number
  losses: number
  win_rate: number
  k_factor: number
  region?: string
}

export interface LoginResponse {
  access_token: string
  refresh_token: string
  user: User
}
