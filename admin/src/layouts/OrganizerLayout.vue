<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore, useAppStore } from '@/stores'

const route = useRoute()
const authStore = useAuthStore()
const appStore = useAppStore()

const pageTitle = computed(() => (route.meta.title as string) || '组织者门户')

const navItems = [
  { path: '/organizer-portal/dashboard', label: '仪表盘', icon: '📊' },
  { path: '/organizer-portal/members', label: '会员管理', icon: '👥' },
  { path: '/organizer-portal/events', label: '赛事发布', icon: '🏆' },
  { path: '/organizer-portal/checkin', label: '签到管理', icon: '✅' },
  { path: '/organizer-portal/scoreboard', label: '实时记分牌', icon: '📋' },
  { path: '/organizer-portal/reports', label: '收入报表', icon: '📈' },
]

function handleLogout() {
  authStore.logout()
  window.location.href = '/login'
}
</script>

<template>
  <div class="min-h-screen flex bg-dark-900">
    <!-- Sidebar -->
    <aside
      class="fixed inset-y-0 left-0 z-30 flex flex-col bg-dark-800 border-r border-dark-600 transition-all duration-300"
      :class="appStore.sidebarCollapsed ? 'w-16' : 'w-64'"
    >
      <!-- Logo -->
      <div class="flex items-center gap-3 px-4 h-16 border-b border-dark-600">
        <div class="w-8 h-8 bg-gold-500 rounded-lg flex items-center justify-center text-dark-900 font-bold text-sm flex-shrink-0">
          组
        </div>
        <span
          v-if="!appStore.sidebarCollapsed"
          class="text-lg font-bold text-gray-100 whitespace-nowrap"
        >
          组织者门户
        </span>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 px-2 py-4 space-y-1 overflow-y-auto">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="sidebar-link"
          :title="appStore.sidebarCollapsed ? item.label : undefined"
        >
          <span class="text-lg flex-shrink-0">{{ item.icon }}</span>
          <span v-if="!appStore.sidebarCollapsed">{{ item.label }}</span>
        </router-link>
      </nav>

      <!-- User section -->
      <div class="px-3 py-4 border-t border-dark-600">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-dark-600 rounded-full flex items-center justify-center text-xs text-gold-400 flex-shrink-0">
            {{ authStore.user?.nickname?.charAt(0) || 'O' }}
          </div>
          <div v-if="!appStore.sidebarCollapsed" class="flex-1 min-w-0">
            <p class="text-sm text-gray-200 truncate">{{ authStore.user?.nickname || '组织者' }}</p>
            <p class="text-xs text-gray-500">赛事组织</p>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main content area -->
    <div
      class="flex-1 flex flex-col transition-all duration-300"
      :class="appStore.sidebarCollapsed ? 'ml-16' : 'ml-64'"
    >
      <!-- Top header -->
      <header class="sticky top-0 z-20 flex items-center justify-between h-16 px-6 bg-dark-800 border-b border-dark-600">
        <div class="flex items-center gap-4">
          <button
            class="p-2 text-gray-400 hover:text-gray-200 rounded-lg hover:bg-dark-600 transition-colors"
            @click="appStore.toggleSidebar"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <h1 class="text-lg font-semibold text-gray-100">{{ pageTitle }}</h1>
        </div>

        <div class="flex items-center gap-3">
          <router-link
            v-if="authStore.isAdmin"
            to="/dashboard"
            class="px-3 py-1.5 text-sm text-gold-400 hover:text-gold-300 rounded-lg hover:bg-dark-600 transition-colors"
          >
            返回管理后台
          </router-link>
          <button
            class="px-3 py-1.5 text-sm text-gray-400 hover:text-red-400 rounded-lg hover:bg-dark-600 transition-colors"
            @click="handleLogout"
          >
            退出登录
          </button>
        </div>
      </header>

      <!-- Page content -->
      <main class="flex-1 p-6">
        <slot />
      </main>
    </div>
  </div>
</template>
