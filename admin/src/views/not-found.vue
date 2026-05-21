<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goHome() {
  router.push('/dashboard')
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-dark-900 px-4">
    <div class="text-center">
      <h1 class="text-6xl font-bold text-gold-500 mb-4">404</h1>
      <p class="text-xl text-gray-300 mb-2">页面未找到</p>
      <p class="text-gray-500 mb-8">您访问的页面不存在或已被移除</p>
      <button class="btn-primary" @click="goHome">返回首页</button>
    </div>
  </div>
</template>
