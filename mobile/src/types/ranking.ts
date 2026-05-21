/**
 * 排行榜相关类型定义
 */

/** 段位等级 */
export type RankTier = 'bronze' | 'silver' | 'gold' | 'platinum' | 'diamond'

/** 个人排行榜条目 */
export interface RankingEntry {
  rank: number
  userId: number
  nickname: string
  avatar?: string
  score: number
  tier: RankTier
  totalMatches: number
  winRate: number
}

/** 俱乐部排行榜条目 */
export interface ClubRanking {
  rank: number
  clubId: number
  clubName: string
  clubLogo?: string
  totalScore: number
  memberCount: number
  eventCount: number
}
