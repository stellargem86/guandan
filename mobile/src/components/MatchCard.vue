<template>
  <view class="match-card card" @click="$emit('click')">
    <view class="match-header">
      <view class="match-status" :class="`status-${match.status}`">
        <text class="status-text">{{ statusLabel }}</text>
      </view>
      <text class="match-time">{{ match.scheduledTime }}</text>
    </view>
    <view class="match-body">
      <text class="match-title">{{ match.title || '掼蛋组局' }}</text>
      <view class="match-meta">
        <text class="meta-item">📍 {{ match.location || '待定' }}</text>
        <text class="meta-item">👥 {{ match.currentPlayers || 0 }}/{{ match.maxPlayers || 4 }}</text>
      </view>
    </view>
    <view v-if="match.tags && match.tags.length" class="match-tags">
      <text v-for="tag in match.tags" :key="tag" class="tag">{{ tag }}</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface MatchCardProps {
  match: {
    id: number | string
    title?: string
    status: 'waiting' | 'full' | 'started' | 'completed' | 'cancelled'
    scheduledTime: string
    location?: string
    currentPlayers?: number
    maxPlayers?: number
    tags?: string[]
  }
}

const props = defineProps<MatchCardProps>()
defineEmits(['click'])

const statusLabel = computed(() => {
  const map: Record<string, string> = {
    waiting: '等待中',
    full: '已满员',
    started: '进行中',
    completed: '已结束',
    cancelled: '已取消',
  }
  return map[props.match.status] || props.match.status
})
</script>

<style scoped>
.match-card {
  margin-bottom: 24rpx;
}

.match-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.match-status {
  padding: 4rpx 16rpx;
  border-radius: 8rpx;
  font-size: 22rpx;
}

.status-waiting {
  background-color: rgba(246, 195, 66, 0.15);
  color: #f6c342;
}

.status-full {
  background-color: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.status-started {
  background-color: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.status-completed {
  background-color: rgba(107, 107, 128, 0.15);
  color: #6b6b80;
}

.status-cancelled {
  background-color: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.match-time {
  font-size: 24rpx;
  color: #b0b0c0;
}

.match-body {
  margin-bottom: 16rpx;
}

.match-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #f5f5f5;
  margin-bottom: 12rpx;
}

.match-meta {
  display: flex;
  gap: 24rpx;
}

.meta-item {
  font-size: 24rpx;
  color: #b0b0c0;
}

.match-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.tag {
  font-size: 22rpx;
  padding: 4rpx 12rpx;
  background-color: #32324a;
  color: #b0b0c0;
  border-radius: 6rpx;
}
</style>
