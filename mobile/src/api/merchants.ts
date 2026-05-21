/**
 * 商户与掼蛋地图相关 API
 */
import { request } from './index'

/** 获取附近商户 */
export function getNearbyMerchants(params: { latitude: number; longitude: number; radius?: number }) {
  return request({
    url: '/api/v1/merchants/nearby',
    method: 'GET',
    data: params,
  })
}

/** 获取商户详情 */
export function getMerchantDetail(id: number) {
  return request({
    url: `/api/v1/merchants/${id}`,
    method: 'GET',
  })
}

/** 获取商户套餐列表 */
export function getMerchantPackages(merchantId: number) {
  return request({
    url: `/api/v1/merchants/${merchantId}/packages`,
    method: 'GET',
  })
}
