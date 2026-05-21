/**
 * 商户相关类型定义
 */

export type MerchantStatus = 'pending' | 'active' | 'suspended'

export interface Merchant {
  id: number
  name: string
  description?: string
  address?: string
  latitude?: number
  longitude?: number
  phone?: string
  rating: number
  cover_image?: string
  photos: string[]
  business_hours?: string
  commission_rate: number
  status: MerchantStatus
  distance?: number // 客户端计算的距离（米）
}

export interface DiningPackage {
  id: number
  merchant_id: number
  name: string
  description?: string
  price: number
  original_price?: number
  cover_image?: string
  validity_days: number
  inventory: number
  sold_count: number
  status: 'active' | 'offline' | 'soldout'
}
