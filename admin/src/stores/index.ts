import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export type UserRole = 'admin' | 'merchant' | 'organizer'

export interface AdminUser {
  id: number
  nickname: string
  avatar_url?: string
  role: UserRole
  merchant_id?: number
  club_id?: number
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('admin_token'))
  const user = ref<AdminUser | null>(
    JSON.parse(localStorage.getItem('admin_user') || 'null')
  )

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isMerchant = computed(() => user.value?.role === 'merchant')
  const isOrganizer = computed(() => user.value?.role === 'organizer')

  function setAuth(newToken: string, newUser: AdminUser) {
    token.value = newToken
    user.value = newUser
    localStorage.setItem('admin_token', newToken)
    localStorage.setItem('admin_user', JSON.stringify(newUser))
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('admin_token')
    localStorage.removeItem('admin_user')
  }

  return {
    token,
    user,
    isAuthenticated,
    isAdmin,
    isMerchant,
    isOrganizer,
    setAuth,
    logout,
  }
})

export const useAppStore = defineStore('app', () => {
  const sidebarCollapsed = ref(false)

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  return {
    sidebarCollapsed,
    toggleSidebar,
  }
})
