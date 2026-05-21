<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores'
import type { AdminUser } from '@/stores'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  if (!username.value || !password.value) {
    error.value = '请输入用户名和密码'
    return
  }

  loading.value = true
  error.value = ''

  try {
    // TODO: Replace with actual API call
    // Simulated login for development
    const mockUser: AdminUser = {
      id: 1,
      nickname: username.value,
      role: 'admin',
    }
    const mockToken = 'dev-token-placeholder'

    authStore.setAuth(mockToken, mockUser)

    const redirect = (route.query.redirect as string) || '/dashboard'
    router.push(redirect)
  } catch {
    error.value = '登录失败，请检查用户名和密码'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-dark-900 px-4">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-gold-500 rounded-2xl mb-4">
          <span class="text-2xl font-bold text-dark-900">掼</span>
        </div>
        <h1 class="text-2xl font-bold text-gray-100">深掼会管理后台</h1>
        <p class="text-sm text-gray-500 mt-2">Shen Guan Hui Admin Platform</p>
      </div>

      <!-- Login form -->
      <form class="card space-y-5" @submit.prevent="handleLogin">
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-1.5">用户名</label>
          <input
            v-model="username"
            type="text"
            class="input-field"
            placeholder="请输入用户名"
            autocomplete="username"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-300 mb-1.5">密码</label>
          <input
            v-model="password"
            type="password"
            class="input-field"
            placeholder="请输入密码"
            autocomplete="current-password"
          />
        </div>

        <p v-if="error" class="text-sm text-red-400">{{ error }}</p>

        <button
          type="submit"
          class="w-full btn-primary py-2.5"
          :disabled="loading"
        >
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
    </div>
  </div>
</template>
