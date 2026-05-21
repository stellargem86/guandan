/**
 * 赛事相关类型定义
 */

export type EventStatus = 'draft' | 'registration' | 'ongoing' | 'completed' | 'cancelled'

export interface GameEvent {
  id: number
  title: string
  description?: string
  organizer_id: number
  organizer_name: string
  location?: string
  start_time: string
  end_time?: string
  registration_fee?: number
  max_participants: number
  current_participants: number
  status: EventStatus
  cover_image?: string
  is_registered: boolean
  created_at: string
}

export interface EventRegistration {
  id: number
  event_id: number
  user_id: number
  status: 'registered' | 'checked_in' | 'cancelled'
  registered_at: string
  checked_in_at?: string
}

/** 赛事详情扩展接口 */
export interface EventDetail extends GameEvent {
  /** 比赛规则（富文本） */
  rules: string
  /** 奖金设置列表 */
  prizeSettings: PrizeSetting[]
  /** 赛程安排 */
  schedule: EventSchedule[]
  /** 报名截止时间 */
  registrationDeadline: string
  /** 保证金 */
  deposit?: number
}

/** 奖金设置 */
export interface PrizeSetting {
  /** 名次 */
  rank: number
  /** 标签（如冠军/亚军/季军） */
  label: string
  /** 奖金金额 */
  amount: number
}

/** 赛程安排 */
export interface EventSchedule {
  /** 轮次 */
  round: number
  /** 开始时间 */
  startTime: string
  /** 描述 */
  description: string
}
