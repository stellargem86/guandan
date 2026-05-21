/**
 * 页面级数据接口定义
 */

import type { Post } from './post'
import type { Merchant } from './merchant'
import type { GameEvent } from './event'
import type { Club, ClubNotice, ClubActivity } from './club'
import type { User } from './user'
import type { MatchCardProps, RankingItemProps } from './ui'

/** 掼友圈首页数据 */
export interface CircleHomeData {
  activeTab: 'latest' | 'friends' | 'map'
  hotMatches: MatchCardProps[]
  posts: Post[]
  isRefreshing: boolean
  hasMore: boolean
}

/** 地图找局页面数据 */
export interface MapPageData {
  activeCategory: 'all' | 'dining' | 'teahouse' | 'chess'
  merchants: Merchant[]
  mapCenter: { latitude: number; longitude: number }
  searchKeyword: string
  mapMarkers: MapMarker[]
}

/** 地图标记点 */
export interface MapMarker {
  id: number
  latitude: number
  longitude: number
  title: string
  iconPath: string
  width: number
  height: number
  callout?: {
    content: string
    display: 'ALWAYS' | 'BYCLICK'
  }
}

/** 赛事列表页面数据 */
export interface EventListData {
  activeTab: 'all' | 'circle' | 'ongoing' | 'ended'
  events: GameEvent[]
  isRefreshing: boolean
  hasMore: boolean
}

/** 天梯榜页面数据 */
export interface RankingsPageData {
  activeTab: 'personal' | 'club'
  activeLevel: 'all' | 'beginner' | 'intermediate' | 'advanced'
  topThree: RankingItemProps[]
  rankings: RankingItemProps[]
  myRanking?: RankingItemProps
}

/** 赛事报名支付页面数据 */
export interface PaymentPageData {
  event: GameEvent
  quantity: number
  registrationFee: number
  deposit: number
  totalAmount: number
  /** 倒计时（秒） */
  countdown: number
  paymentMethod: 'wechat' | 'balance'
  isSubmitting: boolean
}

/** 俱乐部详情页面数据 */
export interface ClubDetailData {
  club: Club
  activeTab: 'notice' | 'activities' | 'achievements' | 'stats'
  notices: ClubNotice[]
  activities: ClubActivity[]
  isMember: boolean
  isApplying: boolean
}

/** 个人中心页面数据 */
export interface ProfilePageData {
  user: User
  stats: {
    points: number
    matches: number
    wins: number
    honor: number
  }
  menuGrid: ProfileMenuItem[]
  menuList: ProfileMenuItem[]
}

/** 个人中心菜单项 */
export interface ProfileMenuItem {
  key: string
  label: string
  icon: string
  badge?: number
  path: string
}
