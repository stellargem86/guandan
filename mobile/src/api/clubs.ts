/**
 * 俱乐部相关 API
 */
import { request } from './index'

/** 获取俱乐部列表 */
export function getClubs(params?: { page?: number; pageSize?: number; region?: string }) {
  return request({
    url: '/api/v1/clubs',
    method: 'GET',
    data: params,
  })
}

/** 获取俱乐部详情 */
export function getClubDetail(id: number) {
  return request({
    url: `/api/v1/clubs/${id}`,
    method: 'GET',
  })
}

/** 申请加入俱乐部 */
export function joinClub(id: number) {
  return request({
    url: `/api/v1/clubs/${id}/join`,
    method: 'POST',
  })
}

/** 获取俱乐部成员 */
export function getClubMembers(id: number) {
  return request({
    url: `/api/v1/clubs/${id}/members`,
    method: 'GET',
  })
}
