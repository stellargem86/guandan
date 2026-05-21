<template>
  <view class="load-more flex items-center justify-center py-4">
    <text v-if="loading" class="text-gray-400 text-sm">加载中...</text>
    <text v-else-if="finished" class="text-gray-300 text-sm">没有更多了</text>
    <text v-else class="text-primary-500 text-sm" @tap="$emit('load')">加载更多</text>
  </view>
</template>

<script setup lang="ts">
defineProps<{
  loading?: boolean
  finished?: boolean
}>()

defineEmits<{
  load: []
}>()
</script>
