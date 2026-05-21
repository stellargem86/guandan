<template>
  <view class="empty-state flex flex-col items-center justify-center py-20">
    <text class="text-gray-400 text-sm">{{ message || '暂无数据' }}</text>
  </view>
</template>

<script setup lang="ts">
defineProps<{
  message?: string
}>()
</script>
