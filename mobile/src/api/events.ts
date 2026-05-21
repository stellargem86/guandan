/**
 * 赛事相关 API
 */
import { request } from './index'

/** 获取赛事列表 */
export function getEvents(params?: { page?: number; pageSize?: number }) {
  return request({
    url: '/api/v1/events',
    method: 'GET',
    data: params,
  })
}

/** 获取赛事详情 */
export function getEventDetail(id: number) {
  return request({
    url: `/api/v1/events/${id}`,
    method: 'GET',
  })
}

/** 赛事报名 */
export function registerEvent(id: number) {
  return request({
    url: `/api/v1/events/${id}/register`,
    method: 'POST',
  })
}

/** 取消报名 */
export function cancelEventRegistration(id: number) {
  return request({
    url: `/api/v1/events/${id}/cancel`,
    method: 'POST',
  })
}
