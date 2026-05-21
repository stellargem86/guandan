<template>
  <view class="page">
    <!-- 成员统计 -->
    <view class="stats-bar">
      <text class="stats-text">共 {{ members.length }} 位成员</text>
    </view>

    <!-- 成员列表 -->
    <scroll-view scroll-y class="member-list">
      <view class="member-item" v-for="member in members" :key="member.id">
        <view class="member-avatar">
          <text class="avatar-text">{{ member.avatar }}</text>
        </view>
        <view class="member-info">
          <view class="member-name-row">
            <text class="member-name">{{ member.name }}</text>
            <view class="role-badge" :class="member.roleClass" v-if="member.role">
              <text class="role-text">{{ member.role }}</text>
            </view>
          </view>
          <view class="member-meta">
            <text class="meta-elo">ELO {{ member.elo }}</text>
            <text class="meta-join">加入: {{ member.joinDate }}</text>
          </view>
        </view>
        <view class="member-stats">
          <text class="win-rate">{{ member.winRate }}%胜率</text>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const members = ref([
  { id: '1', avatar: '张', name: '张会长', role: '会长', roleClass: 'president', elo: 3050, winRate: 78, joinDate: '2022-01' },
  { id: '2', avatar: '李', name: '李副会', role: '副会长', roleClass: 'vice', elo: 2920, winRate: 75, joinDate: '2022-02' },
  { id: '3', avatar: '王', name: '王秘书', role: '秘书', roleClass: 'secretary', elo: 2780, winRate: 72, joinDate: '2022-03' },
  { id: '4', avatar: '陈', name: '陈总', role: '', roleClass: '', elo: 2850, winRate: 74, joinDate: '2022-05' },
  { id: '5', avatar: '刘', name: '刘博士', role: '', roleClass: '', elo: 2720, winRate: 70, joinDate: '2022-06' },
  { id: '6', avatar: '赵', name: '赵老师', role: '', roleClass: '', elo: 2680, winRate: 68, joinDate: '2022-08' },
  { id: '7', avatar: '周', name: '周经理', role: '', roleClass: '', elo: 2650, winRate: 67, joinDate: '2022-09' },
  { id: '8', avatar: '吴', name: '吴教练', role: '', roleClass: '', elo: 2600, winRate: 65, joinDate: '2023-01' },
  { id: '9', avatar: '郑', name: '郑先生', role: '', roleClass: '', elo: 2580, winRate: 64, joinDate: '2023-03' },
  { id: '10', avatar: '孙', name: '孙总监', role: '', roleClass: '', elo: 2550, winRate: 63, joinDate: '2023-05' },
  { id: '11', avatar: '马', name: '马律师', role: '', roleClass: '', elo: 2520, winRate: 62, joinDate: '2023-06' },
  { id: '12', avatar: '朱', name: '朱医生', role: '', roleClass: '', elo: 2480, winRate: 60, joinDate: '2023-08' },
])
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #1a1a2e;
}

.stats-bar {
  padding: 24rpx 32rpx;
  border-bottom: 1rpx solid #3a3a50;
}

.stats-text {
  font-size: 26rpx;
  color: #6b6b80;
}

.member-list {
  height: calc(100vh - 100rpx);
  padding: 16rpx 32rpx;
}

.member-item {
  display: flex;
  align-items: center;
  padding: 24rpx;
  background-color: #2a2a3e;
  border-radius: 16rpx;
  margin-bottom: 12rpx;
}

.member-avatar {
  width: 72rpx;
  height: 72rpx;
  background: linear-gradient(135deg, #3a3a50 0%, #32324a 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16rpx;
}

.avatar-text {
  font-size: 28rpx;
  color: #f5f5f5;
  font-weight: 600;
}

.member-info {
  flex: 1;
}

.member-name-row {
  display: flex;
  align-items: center;
  gap: 10rpx;
  margin-bottom: 8rpx;
}

.member-name {
  font-size: 28rpx;
  color: #f5f5f5;
  font-weight: 500;
}

.role-badge {
  padding: 2rpx 12rpx;
  border-radius: 6rpx;
}

.role-badge.president {
  background-color: rgba(246, 195, 66, 0.15);
}

.role-badge.vice {
  background-color: rgba(59, 130, 246, 0.15);
}

.role-badge.secretary {
  background-color: rgba(16, 185, 129, 0.15);
}

.role-text {
  font-size: 18rpx;
  color: #f6c342;
}

.role-badge.vice .role-text {
  color: #3b82f6;
}

.role-badge.secretary .role-text {
  color: #10b981;
}

.member-meta {
  display: flex;
  gap: 16rpx;
}

.meta-elo {
  font-size: 22rpx;
  color: #f6c342;
}

.meta-join {
  font-size: 22rpx;
  color: #6b6b80;
}

.member-stats {
  flex-shrink: 0;
}

.win-rate {
  font-size: 24rpx;
  color: #10b981;
  font-weight: 500;
}
</style>
