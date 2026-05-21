/**
 * 认证相关组合函数
 */
import { computed } from 'vue'
import { useUserStore } from '../stores/user'

export function useAuth() {
  const userStore = useUserStore()

  const isLoggedIn = computed(() => !!userStore.token)
  const currentUser = computed(() => userStore.userInfo)

  /** 微信登录 */
  async function loginWithWechat() {
    // TODO: 实现微信登录逻辑
    return Promise.resolve()
  }

  /** 退出登录 */
  function logout() {
    userStore.clearUser()
    uni.reLaunch({ url: '/pages/common/login' })
  }

  /** 检查登录状态 */
  function checkAuth(): boolean {
    if (!isLoggedIn.value) {
      uni.navigateTo({ url: '/pages/common/login' })
      return false
    }
    return true
  }

  return {
    isLoggedIn,
    currentUser,
    loginWithWechat,
    logout,
    checkAuth,
  }
}
