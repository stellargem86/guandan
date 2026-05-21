/**
 * 订单与支付相关 API
 */
import { request } from './index'

/** 创建订单 */
export function createOrder(data: { orderType: string; targetId: number; amount: number }) {
  return request({
    url: '/api/v1/orders',
    method: 'POST',
    data,
  })
}

/** 获取订单详情 */
export function getOrderDetail(id: number) {
  return request({
    url: `/api/v1/orders/${id}`,
    method: 'GET',
  })
}

/** 发起支付 */
export function payOrder(id: number) {
  return request({
    url: `/api/v1/orders/${id}/pay`,
    method: 'POST',
  })
}

/** 申请退款 */
export function refundOrder(id: number) {
  return request({
    url: `/api/v1/orders/${id}/refund`,
    method: 'POST',
  })
}
