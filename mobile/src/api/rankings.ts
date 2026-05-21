/**
 * 天梯排行榜相关 API
 */
import { request } from './index'

/** 个人排行榜 */
export function getPersonalRankings(params?: { page?: number; pageSize?: number }) {
  return request({
    url: '/api/v1/rankings/personal',
    method: 'GET',
    data: params,
  })
}

/** 俱乐部排行榜 */
export function getClubRankings(params?: { page?: number; pageSize?: number }) {
  return request({
    url: '/api/v1/rankings/club',
    method: 'GET',
    data: params,
  })
}

/** 地区排行榜 */
export function getRegionalRankings(params?: { page?: number; pageSize?: number; region?: string }) {
  return request({
    url: '/api/v1/rankings/regional',
    method: 'GET',
    data: params,
  })
}

/** 获取用户 ELO 详情 */
export function getUserElo(userId: number) {
  return request({
    url: `/api/v1/users/${userId}/elo`,
    method: 'GET',
  })
}
