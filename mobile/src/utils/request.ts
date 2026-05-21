/**
 * uni-app 请求封装
 * 统一处理 Token、拦截器、错误处理
 */

const BASE_URL = '' // 通过环境变量配置

interface RequestOptions {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: Record<string, unknown>
  header?: Record<string, string>
  showLoading?: boolean
  showError?: boolean
}

interface ApiResponse<T = unknown> {
  code: number
  data: T
  message: string
}

function getToken(): string {
  return uni.getStorageSync('token') || ''
}

export function request<T = unknown>(options: RequestOptions): Promise<ApiResponse<T>> {
  const { url, method = 'GET', data, header = {}, showLoading = false, showError = true } = options

  if (showLoading) {
    uni.showLoading({ title: '加载中...' })
  }

  const token = getToken()
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...header,
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  return new Promise((resolve, reject) => {
    uni.request({
      url: `${BASE_URL}${url}`,
      method,
      data,
      header: headers,
      success: (res) => {
        if (showLoading) uni.hideLoading()

        const statusCode = res.statusCode
        if (statusCode === 200) {
          resolve(res.data as ApiResponse<T>)
        } else if (statusCode === 401) {
          // Token 过期，跳转登录
          uni.removeStorageSync('token')
          uni.navigateTo({ url: '/pages/common/login' })
          reject(new Error('未授权，请重新登录'))
        } else {
          const errorMsg = (res.data as ApiResponse).message || '请求失败'
          if (showError) {
            uni.showToast({ title: errorMsg, icon: 'none' })
          }
          reject(new Error(errorMsg))
        }
      },
      fail: (err) => {
        if (showLoading) uni.hideLoading()
        if (showError) {
          uni.showToast({ title: '网络异常，请稍后重试', icon: 'none' })
        }
        reject(err)
      },
    })
  })
}

export default request
