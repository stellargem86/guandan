<template>
  <view class="page">
    <!-- 用户卡片 -->
    <view class="user-card">
      <view class="user-info-row">
        <view class="user-avatar">
          <text class="avatar-text">陈</text>
        </view>
        <view class="user-details">
          <text class="user-name">陈总·科技</text>
          <text class="user-id">深掼会 ID: SGH-2024-0086</text>
        </view>
        <view class="edit-btn">
          <text class="edit-text">编辑</text>
        </view>
      </view>

      <!-- 数据统计 -->
      <view class="user-stats">
        <view class="stat-item">
          <text class="stat-value gold">2680</text>
          <text class="stat-label">ELO分</text>
        </view>
        <view class="stat-divider"></view>
        <view class="stat-item">
          <text class="stat-value">128</text>
          <text class="stat-label">场次</text>
        </view>
        <view class="stat-divider"></view>
        <view class="stat-item">
          <text class="stat-value green">62%</text>
          <text class="stat-label">胜率</text>
        </view>
        <view class="stat-divider"></view>
        <view class="stat-item">
          <text class="stat-value">A+</text>
          <text class="stat-label">段位</text>
        </view>
      </view>
    </view>

    <!-- 钱包卡片 -->
    <view class="wallet-card" @tap="goWallet">
      <view class="wallet-left">
        <text class="wallet-icon">💰</text>
        <view class="wallet-info">
          <text class="wallet-label">我的钱包</text>
          <text class="wallet-balance">¥ 680.00</text>
        </view>
      </view>
      <view class="wallet-action">
        <text class="wallet-arrow">›</text>
      </view>
    </view>

    <!-- 功能菜单 -->
    <view class="menu-section">
      <view class="menu-item" v-for="item in menuItems" :key="item.title" @tap="handleMenu(item)">
        <view class="menu-left">
          <text class="menu-icon">{{ item.icon }}</text>
          <text class="menu-title">{{ item.title }}</text>
        </view>
        <view class="menu-right">
          <text class="menu-badge" v-if="item.badge">{{ item.badge }}</text>
          <text class="menu-arrow">›</text>
        </view>
      </view>
    </view>

    <!-- 成就徽章预览 -->
    <view class="badges-section">
      <view class="badges-header">
        <text class="badges-title">荣誉徽章</text>
        <text class="badges-more" @tap="goBadges">查看全部 ›</text>
      </view>
      <view class="badges-list">
        <view class="badge-item" v-for="badge in badges" :key="badge.name">
          <text class="badge-emoji">{{ badge.emoji }}</text>
          <text class="badge-name">{{ badge.name }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const menuItems = ref([
  { icon: '🏆', title: '赛事记录', badge: '3', path: '/pages/profile/orders' },
  { icon: '🛒', title: '购买记录', badge: '', path: '/pages/profile/orders' },
  { icon: '🏅', title: '荣誉徽章', badge: '12', path: '/pages/profile/badges' },
  { icon: '👥', title: '找掼友', badge: '', path: '' },
  { icon: '📊', title: '数据分析', badge: '', path: '' },
  { icon: '⚙️', title: '设置', badge: '', path: '/pages/profile/settings' },
])

const badges = ref([
  { emoji: '🥇', name: '首胜' },
  { emoji: '🔥', name: '连胜5场' },
  { emoji: '⭐', name: 'A段位' },
  { emoji: '🎯', name: '精准出牌' },
  { emoji: '💎', name: 'VIP会员' },
])

function goWallet() {
  uni.navigateTo({ url: '/pages/profile/wallet' })
}

function goBadges() {
  uni.navigateTo({ url: '/pages/profile/badges' })
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
  background-color: #1a1a2e;
  padding: 32rpx;
  padding-bottom: 120rpx;
}

/* 用户卡片 */
.user-card {
  background-color: #2a2a3e;
  border-radius: 24rpx;
  padding: 28rpx;
  margin-bottom: 24rpx;
}

.user-info-row {
  display: flex;
  align-items: center;
  margin-bottom: 28rpx;
}

.user-avatar {
  width: 96rpx;
  height: 96rpx;
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20rpx;
}

.avatar-text {
  font-size: 36rpx;
  color: #1a1a2e;
  font-weight: 700;
}

.user-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6rpx;
}

.user-name {
  font-size: 32rpx;
  font-weight: 700;
  color: #f5f5f5;
}

.user-id {
  font-size: 22rpx;
  color: #6b6b80;
}

.edit-btn {
  border: 1rpx solid #3a3a50;
  border-radius: 20rpx;
  padding: 10rpx 24rpx;
}

.edit-text {
  font-size: 24rpx;
  color: #b0b0c0;
}

.user-stats {
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding-top: 24rpx;
  border-top: 1rpx solid #3a3a50;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6rpx;
}

.stat-value {
  font-size: 32rpx;
  font-weight: 700;
  color: #f5f5f5;
}

.stat-value.gold {
  color: #f6c342;
}

.stat-value.green {
  color: #10b981;
}

.stat-label {
  font-size: 22rpx;
  color: #6b6b80;
}

.stat-divider {
  width: 1rpx;
  height: 48rpx;
  background-color: #3a3a50;
}

/* 钱包卡片 */
.wallet-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, rgba(246, 195, 66, 0.08) 0%, rgba(246, 195, 66, 0.03) 100%);
  border: 1rpx solid rgba(246, 195, 66, 0.15);
  border-radius: 20rpx;
  padding: 28rpx;
  margin-bottom: 24rpx;
}

.wallet-left {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.wallet-icon {
  font-size: 40rpx;
}

.wallet-info {
  display: flex;
  flex-direction: column;
  gap: 4rpx;
}

.wallet-label {
  font-size: 24rpx;
  color: #6b6b80;
}

.wallet-balance {
  font-size: 36rpx;
  font-weight: 700;
  color: #f6c342;
}

.wallet-action {
  padding: 0 8rpx;
}

.wallet-arrow {
  font-size: 36rpx;
  color: #6b6b80;
}

/* 菜单 */
.menu-section {
  background-color: #2a2a3e;
  border-radius: 20rpx;
  margin-bottom: 24rpx;
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 28rpx 24rpx;
  border-bottom: 1rpx solid #3a3a50;
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
  color: #f5f5f5;
}

.menu-right {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.menu-badge {
  font-size: 20rpx;
  color: #f6c342;
  background-color: rgba(246, 195, 66, 0.12);
  border-radius: 16rpx;
  padding: 4rpx 14rpx;
}

.menu-arrow {
  font-size: 32rpx;
  color: #6b6b80;
}

/* 徽章 */
.badges-section {
  background-color: #2a2a3e;
  border-radius: 20rpx;
  padding: 24rpx;
}

.badges-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20rpx;
}

.badges-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #f5f5f5;
}

.badges-more {
  font-size: 24rpx;
  color: #f6c342;
}

.badges-list {
  display: flex;
  gap: 24rpx;
}

.badge-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
}

.badge-emoji {
  font-size: 40rpx;
}

.badge-name {
  font-size: 20rpx;
  color: #6b6b80;
}
</style>
