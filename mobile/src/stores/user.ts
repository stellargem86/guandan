/**
 * 用户状态管理
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'

interface UserInfo {
  id: number
  platformId: string
  nickname: string
  avatarUrl: string
}

export const useUserStore = defineStore('user', () => {
  const token = ref<string>('')
  const refreshToken = ref<string>('')
  const userInfo = ref<UserInfo | null>(null)

  function setToken(accessToken: string, refresh: string) {
    token.value = accessToken
    refreshToken.value = refresh
    uni.setStorageSync('token', accessToken)
    uni.setStorageSync('refreshToken', refresh)
  }

  function setUser(user: UserInfo) {
    userInfo.value = user
    uni.setStorageSync('userInfo', JSON.stringify(user))
  }

  function clearUser() {
    token.value = ''
    refreshToken.value = ''
    userInfo.value = null
    uni.removeStorageSync('token')
    uni.removeStorageSync('refreshToken')
    uni.removeStorageSync('userInfo')
  }

  /** 从本地存储恢复状态 */
  function restore() {
    token.value = uni.getStorageSync('token') || ''
    refreshToken.value = uni.getStorageSync('refreshToken') || ''
    const stored = uni.getStorageSync('userInfo')
    if (stored) {
      try {
        userInfo.value = JSON.parse(stored)
      } catch {
        userInfo.value = null
      }
    }
  }

  return {
    token,
    refreshToken,
    userInfo,
    setToken,
    setUser,
    clearUser,
    restore,
  }
})
