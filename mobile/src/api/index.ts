/**
 * API 请求层统一封装
 * 基于 uni.request 封装的 HTTP 请求工具
 */

import { useUserStore } from '../stores/user'

const BASE_URL = '' // TODO: 配置 API 基础地址

interface RequestOptions {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: Record<string, unknown>
  headers?: Record<string, string>
}

interface ApiResponse<T = unknown> {
  code: number
  data: T
  message: string
}

export async function request<T = unknown>(options: RequestOptions): Promise<ApiResponse<T>> {
  const userStore = useUserStore()
  const token = userStore.token

  const header: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.headers,
  }

  if (token) {
    header['Authorization'] = `Bearer ${token}`
  }

  return new Promise((resolve, reject) => {
    uni.request({
      url: `${BASE_URL}${options.url}`,
      method: options.method || 'GET',
      data: options.data,
      header,
      success: (res) => {
        const data = res.data as ApiResponse<T>
        if (data.code === 0) {
          resolve(data)
        } else if (data.code === 401) {
          // Token 过期，跳转登录
          uni.navigateTo({ url: '/pages/common/login' })
          reject(new Error('Unauthorized'))
        } else {
          reject(new Error(data.message || 'Request failed'))
        }
      },
      fail: (err) => {
        reject(new Error(err.errMsg || 'Network error'))
      },
    })
  })
}

export default request
