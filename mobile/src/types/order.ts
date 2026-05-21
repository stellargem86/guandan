/**
 * 订单和支付相关类型定义
 */

export type OrderType =
  | 'dining_package'
  | 'event_reg'
  | 'club_membership'
  | 'matchmaking_deposit'
  | 'withdrawal'

export type OrderStatus = 'pending' | 'paid' | 'refunded' | 'cancelled' | 'failed'

export interface Order {
  id: number
  order_no: string
  user_id: number
  order_type: OrderType
  target_id?: number
  amount: number
  status: OrderStatus
  paid_at?: string
  refunded_at?: string
  verification_code?: string
  verification_qr_url?: string
  verified_at?: string
  expires_at?: string
  created_at: string
}

export interface WalletInfo {
  balance: number
  frozen_amount: number
  total_income: number
  total_expense: number
}

export interface WalletTransaction {
  id: number
  type: 'income' | 'expense' | 'withdraw' | 'refund'
  amount: number
  description: string
  created_at: string
}
