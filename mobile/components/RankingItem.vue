<template>
  <view class="ranking-item" @click="$emit('click')">
    <view class="rank-number" :class="{ 'rank-top': rank <= 3 }">
      <text v-if="rank <= 3" class="rank-medal">{{ medalEmoji }}</text>
      <text v-else class="rank-text">{{ rank }}</text>
    </view>
    <image v-if="item.avatar" :src="item.avatar" class="rank-avatar" mode="aspectFill" />
    <view v-else class="rank-avatar rank-avatar-placeholder">
      <text class="placeholder-text">👤</text>
    </view>
    <view class="rank-info">
      <text class="rank-name">{{ item.name }}</text>
      <text class="rank-tier">{{ item.tier || '' }}</text>
    </view>
    <view class="rank-score">
      <text class="score-value">{{ item.score }}</text>
      <text class="score-label">ELO</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface RankingItemProps {
  rank: number
  item: {
    id: number | string
    name: string
    avatar?: string
    score: number
    tier?: string
  }
}

const props = defineProps<RankingItemProps>()
defineEmits(['click'])

const medalEmoji = computed(() => {
  const medals: Record<number, string> = { 1: '🥇', 2: '🥈', 3: '🥉' }
  return medals[props.rank] || ''
})
</script>

<style scoped>
.ranking-item {
  display: flex;
  align-items: center;
  padding: 20rpx 24rpx;
  gap: 20rpx;
  border-bottom: 1rpx solid #3a3a50;
}

.ranking-item:last-child {
  border-bottom: none;
}

.rank-number {
  width: 48rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.rank-medal {
  font-size: 36rpx;
}

.rank-text {
  font-size: 28rpx;
  color: #6b6b80;
  font-weight: 600;
}

.rank-avatar {
  width: 72rpx;
  height: 72rpx;
  border-radius: 50%;
}

.rank-avatar-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #32324a;
}

.placeholder-text {
  font-size: 32rpx;
}

.rank-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6rpx;
}

.rank-name {
  font-size: 28rpx;
  color: #f5f5f5;
  font-weight: 500;
}

.rank-tier {
  font-size: 22rpx;
  color: #f6c342;
}

.rank-score {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4rpx;
}

.score-value {
  font-size: 30rpx;
  color: #f6c342;
  font-weight: 700;
}

.score-label {
  font-size: 20rpx;
  color: #6b6b80;
}
</style>
