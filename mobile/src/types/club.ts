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

/** 俱乐部详情扩展接口 */
export interface ClubDetail extends Club {
  /** 公告列表 */
  announcements: ClubNotice[]
  /** 活动列表 */
  activities: ClubActivity[]
  /** 成就列表 */
  achievements: ClubAchievement[]
  /** 统计数据 */
  stats: ClubStats
}

/** 俱乐部公告 */
export interface ClubNotice {
  id: number
  clubId: number
  title: string
  content: string
  createdAt: string
  isPinned: boolean
}

/** 俱乐部成就 */
export interface ClubAchievement {
  id: number
  title: string
  description: string
  icon: string
  unlockedAt?: string
}

/** 俱乐部统计 */
export interface ClubStats {
  totalMembers: number
  totalEvents: number
  totalMatches: number
  avgScore: number
}

/** 俱乐部聊天消息 */
export interface ClubChatMessage {
  id: number
  clubId: number
  userId: number
  userNickname: string
  userAvatar?: string
  content: string
  type: 'text' | 'image' | 'system'
  createdAt: string
}
