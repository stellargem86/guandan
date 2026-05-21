/**
 * 本地存储工具
 * 封装 uni-app Storage API
 */

export const storage = {
  get<T = string>(key: string): T | null {
    try {
      const value = uni.getStorageSync(key)
      if (!value) return null
      return JSON.parse(value) as T
    } catch {
      return uni.getStorageSync(key) as T | null
    }
  },

  set(key: string, value: unknown): void {
    if (typeof value === 'string') {
      uni.setStorageSync(key, value)
    } else {
      uni.setStorageSync(key, JSON.stringify(value))
    }
  },

  remove(key: string): void {
    uni.removeStorageSync(key)
  },

  clear(): void {
    uni.clearStorageSync()
  },
}

export default storage
