/**
 * 一键组局相关 API
 */
import { request } from './index'

/** 创建组局 */
export function createMatchmaking(data: {
  time: string
  locationName: string
  latitude: number
  longitude: number
  skillLevel: string
  industry?: string
  maxPlayers: number
}) {
  return request({
    url: '/api/v1/matchmaking',
    method: 'POST',
    data,
  })
}

/** 获取组局列表 */
export function getMatchmakingList(params?: {
  page?: number
  pageSize?: number
  rankRange?: string
  distance?: number
}) {
  return request({
    url: '/api/v1/matchmaking',
    method: 'GET',
    data: params,
  })
}

/** 加入组局 */
export function joinMatchmaking(id: number) {
  return request({
    url: `/api/v1/matchmaking/${id}/join`,
    method: 'POST',
  })
}

/** 取消参加 */
export function cancelMatchmaking(id: number) {
  return request({
    url: `/api/v1/matchmaking/${id}/cancel`,
    method: 'POST',
  })
}
