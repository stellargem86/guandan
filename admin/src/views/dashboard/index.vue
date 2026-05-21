<script setup lang="ts">
</script>

<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-100 mb-4">仪表盘</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <div class="card">
        <p class="text-sm text-gray-400">今日活跃用户</p>
        <p class="text-2xl font-bold text-gold-400 mt-1">--</p>
      </div>
      <div class="card">
        <p class="text-sm text-gray-400">今日收入</p>
        <p class="text-2xl font-bold text-gold-400 mt-1">--</p>
      </div>
      <div class="card">
        <p class="text-sm text-gray-400">进行中赛事</p>
        <p class="text-2xl font-bold text-gold-400 mt-1">--</p>
      </div>
      <div class="card">
        <p class="text-sm text-gray-400">待审核内容</p>
        <p class="text-2xl font-bold text-gold-400 mt-1">--</p>
      </div>
    </div>
    <p class="text-gray-500">平台核心数据概览，连接后端后将展示实时数据</p>
  </div>
</template>
