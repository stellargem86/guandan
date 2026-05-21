/**
 * UI 组件 Props 接口定义
 */

import type { EventStatus } from './event'

/** 通用卡片组件 Props */
export interface CardProps {
  padding?: string
  radius?: 'sm' | 'md' | 'lg'
  shadow?: 'sm' | 'md' | 'lg'
  border?: boolean
}

/** 标签页项目 */
export interface TabItem {
  key: string
  label: string
  badge?: number
}

/** 标签页组件 Props */
export interface TabBarProps {
  items: TabItem[]
  activeKey: string
  scrollable?: boolean
  lineStyle?: 'underline' | 'background'
}

/** 约局卡片组件 Props */
export interface MatchCardProps {
  id: number
  title: string
  hostAvatar: string
  hostName: string
  time: string
  location: string
  currentPlayers: number
  maxPlayers: number
  tags: string[]
  status: 'open' | 'full' | 'started' | 'ended'
}

/** 商户卡片组件 Props */
export interface MerchantCardProps {
  id: number
  name: string
  coverImage: string
  rating: number
  pricePerPerson?: number
  distance?: string
  tags: string[]
  address: string
}

/** 赛事卡片组件 Props */
export interface EventCardProps {
  id: number
  title: string
  coverImage?: string
  startTime: string
  location: string
  prizePool: number
  registrationFee: number
  currentParticipants: number
  maxParticipants: number
  status: EventStatus
}

/** 排行榜项目组件 Props */
export interface RankingItemProps {
  rank: number
  userId: number
  avatar: string
  nickname: string
  score: number
  tier: string
  /** 前三名高亮 */
  isHighlighted?: boolean
}

/** 俱乐部卡片组件 Props */
export interface ClubCardProps {
  id: number
  name: string
  logo: string
  memberCount: number
  location: string
  tags: string[]
  description: string
}

/** 资讯文章卡片组件 Props */
export interface ArticleCardProps {
  id: number
  title: string
  thumbnail?: string
  source: string
  publishTime: string
  viewCount: number
  likeCount: number
  category: string
}

/** 支付按钮组件 Props */
export interface PaymentButtonProps {
  amount: number
  label: string
  loading?: boolean
  disabled?: boolean
  /** 倒计时秒数 */
  countdown?: number
}
