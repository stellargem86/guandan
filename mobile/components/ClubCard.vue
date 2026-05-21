<template>
  <view class="club-card card" @click="$emit('click')">
    <view class="club-header">
      <image v-if="club.coverImage" :src="club.coverImage" class="club-avatar" mode="aspectFill" />
      <view v-else class="club-avatar club-avatar-placeholder">
        <text class="placeholder-text">🏆</text>
      </view>
      <view class="club-info">
        <text class="club-name">{{ club.name }}</text>
        <text class="club-members">{{ club.memberCount || 0 }} 成员</text>
      </view>
    </view>
    <text v-if="club.description" class="club-desc">{{ club.description }}</text>
  </view>
</template>

<script setup lang="ts">
interface ClubCardProps {
  club: {
    id: number | string
    name: string
    coverImage?: string
    memberCount?: number
    description?: string
  }
}

defineProps<ClubCardProps>()
defineEmits(['click'])
</script>

<style scoped>
.club-card {
  margin-bottom: 24rpx;
}

.club-header {
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.club-avatar {
  width: 88rpx;
  height: 88rpx;
  border-radius: 16rpx;
}

.club-avatar-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #32324a;
}

.placeholder-text {
  font-size: 40rpx;
}

.club-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.club-name {
  font-size: 30rpx;
  font-weight: 600;
  color: #f5f5f5;
}

.club-members {
  font-size: 24rpx;
  color: #6b6b80;
}

.club-desc {
  margin-top: 16rpx;
  font-size: 26rpx;
  color: #b0b0c0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
