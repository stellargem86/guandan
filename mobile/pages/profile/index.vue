<template>
  <view class="page">
    <!-- 用户信息卡片 -->
    <view class="user-card">
      <view class="user-bg"></view>
      <view class="user-content">
        <view class="user-row">
          <view class="user-avatar">
            <text class="avatar-char">掼</text>
          </view>
          <view class="user-info">
            <text class="user-name">掼蛋小王子</text>
            <text class="user-id">ID:10085</text>
          </view>
        </view>
        <!-- 统计数据 -->
        <view class="user-stats">
          <view class="stat-item">
            <text class="stat-value">2680</text>
            <text class="stat-label">积分</text>
          </view>
          <view class="stat-item">
            <text class="stat-value">12</text>
            <text class="stat-label">赛事</text>
          </view>
          <view class="stat-item">
            <text class="stat-value">5</text>
            <text class="stat-label">荣誉</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 功能网格 -->
    <view class="function-grid">
      <view class="grid-item" v-for="item in gridItems" :key="item.title" @tap="handleGridTap(item)">
        <view class="grid-icon-wrap">
          <text class="grid-icon">{{ item.icon }}</text>
        </view>
        <text class="grid-label">{{ item.title }}</text>
      </view>
    </view>

    <!-- 菜单列表 -->
    <view class="menu-section">
      <view class="menu-item" v-for="item in menuItems" :key="item.title" @tap="handleMenu(item)">
        <view class="menu-left">
          <text class="menu-icon">{{ item.icon }}</text>
          <text class="menu-title">{{ item.title }}</text>
        </view>
        <text class="menu-arrow">›</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const gridItems = ref([
  { icon: '🏆', title: '我的赛事', path: '/pages/profile/orders' },
  { icon: '💰', title: '我的钱包', path: '/pages/profile/wallet' },
  { icon: '🏅', title: '荣誉徽章', path: '/pages/profile/badges' },
  { icon: '📊', title: '数据分析', path: '' },
])

const menuItems = ref([
  { icon: '🎯', title: '我的俱乐部', path: '/pages/clubs/detail?id=1' },
  { icon: '📋', title: '报名记录', path: '/pages/profile/orders' },
  { icon: '👥', title: '掼蛋好友', path: '' },
  { icon: '🔔', title: '消息通知', path: '' },
  { icon: '💳', title: '掼蛋交大厅', path: '' },
  { icon: '🛡️', title: '隐私安全', path: '' },
  { icon: '⚙️', title: '设置', path: '/pages/profile/settings' },
])

function handleGridTap(item: any) {
  if (item.path) {
    uni.navigateTo({ url: item.path })
  } else {
    uni.showToast({ title: '功能开发中', icon: 'none' })
  }
}

function handleMenu(item: any) {
  if (item.path) {
    uni.navigateTo({ url: item.path })
  } else {
    uni.showToast({ title: '功能开发中', icon: 'none' })
  }
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #F5F5F5;
  padding-bottom: 120rpx;
}

/* 用户卡片 */
.user-card {
  position: relative;
  margin-bottom: 16rpx;
}

.user-bg {
  height: 200rpx;
  background: linear-gradient(135deg, #C41E3A 0%, #A01830 100%);
}

.user-content {
  background-color: #FFFFFF;
  margin: -60rpx 24rpx 0;
  border-radius: 16rpx;
  padding: 24rpx;
  position: relative;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.08);
}

.user-row {
  display: flex;
  align-items: center;
  margin-bottom: 24rpx;
}

.user-avatar {
  width: 96rpx;
  height: 96rpx;
  background-color: #C41E3A;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20rpx;
  border: 4rpx solid #FFFFFF;
  box-shadow: 0 4rpx 12rpx rgba(196, 30, 58, 0.3);
}

.avatar-char {
  font-size: 36rpx;
  color: #FFFFFF;
  font-weight: 700;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 32rpx;
  font-weight: 700;
  color: #333333;
  margin-bottom: 4rpx;
}

.user-id {
  font-size: 24rpx;
  color: #999999;
}

/* 统计 */
.user-stats {
  display: flex;
  justify-content: space-around;
  padding-top: 20rpx;
  border-top: 1rpx solid #F0F0F0;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4rpx;
}

.stat-value {
  font-size: 32rpx;
  font-weight: 700;
  color: #C41E3A;
}

.stat-label {
  font-size: 22rpx;
  color: #999999;
}

/* 功能网格 */
.function-grid {
  display: flex;
  background-color: #FFFFFF;
  padding: 24rpx;
  margin: 0 24rpx 16rpx;
  border-radius: 16rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.grid-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12rpx;
}

.grid-icon-wrap {
  width: 80rpx;
  height: 80rpx;
  background-color: #FFF0F0;
  border-radius: 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.grid-icon {
  font-size: 36rpx;
}

.grid-label {
  font-size: 24rpx;
  color: #333333;
}

/* 菜单列表 */
.menu-section {
  background-color: #FFFFFF;
  margin: 0 24rpx;
  border-radius: 16rpx;
  overflow: hidden;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 28rpx 24rpx;
  border-bottom: 1rpx solid #F5F5F5;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-left {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.menu-icon {
  font-size: 32rpx;
}

.menu-title {
  font-size: 28rpx;
  color: #333333;
}

.menu-arrow {
  font-size: 28rpx;
  color: #CCCCCC;
}
</style>
