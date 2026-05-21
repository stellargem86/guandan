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
