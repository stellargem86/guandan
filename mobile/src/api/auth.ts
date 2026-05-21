/**
 * 认证相关 API
 */
import { request } from './index'

export interface WechatLoginParams {
  code: string
}

export interface LoginResponse {
  accessToken: string
  refreshToken: string
  user: {
    id: number
    platformId: string
    nickname: string
    avatarUrl: string
  }
}

/** 微信授权登录 */
export function wechatLogin(params: WechatLoginParams) {
  return request<LoginResponse>({
    url: '/api/v1/auth/wechat-login',
    method: 'POST',
    data: params,
  })
}

/** 刷新 Token */
export function refreshToken(token: string) {
  return request<{ accessToken: string }>({
    url: '/api/v1/auth/refresh-token',
    method: 'POST',
    data: { refreshToken: token },
  })
}

/** 获取当前用户信息 */
export function getCurrentUser() {
  return request<LoginResponse['user']>({
    url: '/api/v1/auth/me',
    method: 'GET',
  })
}
