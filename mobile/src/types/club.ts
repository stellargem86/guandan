/**
 * 俱乐部相关类型定义
 */

export interface Club {
  id: number
  name: string
  description?: string
  cover_image?: string
  owner_id: number
  owner_name: string
  member_count: number
  max_members: number
  membership_fee?: number
  region?: string
  status: 'active' | 'suspended'
  is_member: boolean
  created_at: string
}

export interface ClubMember {
  id: number
  club_id: number
  user_id: number
  user_nickname: string
  user_avatar?: string
  role: 'owner' | 'admin' | 'member'
  elo_score?: number
  joined_at: string
}

export interface ClubActivity {
  id: number
  club_id: number
  title: string
  description?: string
  start_time: string
  location?: string
  max_participants?: number
  current_participants: number
  created_at: string
}
