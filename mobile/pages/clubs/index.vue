<template>
  <view class="page">
    <!-- 搜索栏 -->
    <view class="search-section">
      <view class="search-bar">
        <text class="search-icon">🔍</text>
        <input
          class="search-input"
          placeholder="搜索俱乐部名称"
          placeholder-class="search-placeholder"
          v-model="searchText"
        />
      </view>
    </view>

    <!-- 快捷入口 -->
    <view class="quick-entry">
      <view class="entry-item" @tap="goMyClub">
        <text class="entry-icon">🏠</text>
        <text class="entry-text">我的俱乐部</text>
      </view>
      <view class="entry-item" @tap="goCreate">
        <text class="entry-icon">➕</text>
        <text class="entry-text">创建俱乐部</text>
      </view>
    </view>

    <!-- 推荐俱乐部 -->
    <view class="section-header">
      <text class="section-title">推荐俱乐部</text>
    </view>

    <scroll-view scroll-y class="club-list">
      <view class="club-card" v-for="club in clubs" :key="club.id" @tap="goDetail(club.id)">
        <view class="club-avatar">
          <text class="club-emoji">{{ club.emoji }}</text>
        </view>
        <view class="club-info">
          <view class="club-name-row">
            <text class="club-name">{{ club.name }}</text>
            <view class="club-level" v-if="club.level">
              <text class="level-text">{{ club.level }}</text>
            </view>
          </view>
          <view class="club-meta">
            <text class="meta-members">👥 {{ club.members }}/{{ club.maxMembers }}</text>
            <text class="meta-region">📍 {{ club.region }}</text>
          </view>
          <view class="club-stats">
            <text class="stat-item">ELO均分: {{ club.avgElo }}</text>
            <text class="stat-item">活跃: {{ club.activeRate }}%</text>
          </view>
        </view>
        <view class="join-btn" @tap.stop="handleJoin(club)">
          <text class="join-text">申请加入</text>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const searchText = ref('')

const clubs = ref([
  {
    id: '1',
    name: '金陵掼蛋俱乐部',
    emoji: '🏆',
    members: 128,
    maxMembers: 200,
    region: '南京·建邺',
    avgElo: 2680,
    activeRate: 85,
    level: '钻石',
  },
  {
    id: '2',
    name: '龙虎山精英会',
    emoji: '🐉',
    members: 96,
    maxMembers: 150,
    region: '南京·鼓楼',
    avgElo: 2520,
    activeRate: 78,
    level: '铂金',
  },
  {
    id: '3',
    name: '紫金掼蛋社',
    emoji: '💜',
    members: 64,
    maxMembers: 100,
    region: '南京·玄武',
    avgElo: 2350,
    activeRate: 72,
    level: '黄金',
  },
  {
    id: '4',
    name: '秦淮商会牌友团',
    emoji: '🏮',
    members: 156,
    maxMembers: 200,
    region: '南京·秦淮',
    avgElo: 2780,
    activeRate: 90,
    level: '钻石',
  },
  {
    id: '5',
    name: '江宁新手训练营',
    emoji: '🌟',
    members: 48,
    maxMembers: 80,
    region: '南京·江宁',
    avgElo: 1800,
    activeRate: 65,
    level: '白银',
  },
])

function goDetail(id: string) {
  uni.navigateTo({ url: `/pages/clubs/detail?id=${id}` })
}

function goMyClub() {
  uni.navigateTo({ url: '/pages/clubs/detail?id=1' })
}

function goCreate() {
  uni.navigateTo({ url: '/pages/clubs/create' })
}

function handleJoin(club: any) {
  uni.showToast({ title: `已申请加入「${club.name}」`, icon: 'none' })
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #1a1a2e;
  padding-bottom: 120rpx;
}

.search-section {
  padding: 24rpx 32rpx 16rpx;
}

.search-bar {
  display: flex;
  align-items: center;
  background-color: #2a2a3e;
  border-radius: 40rpx;
  padding: 18rpx 28rpx;
  gap: 12rpx;
}

.search-icon {
  font-size: 28rpx;
}

.search-input {
  flex: 1;
  font-size: 28rpx;
  color: #f5f5f5;
}

.search-placeholder {
  color: #6b6b80;
}

/* 快捷入口 */
.quick-entry {
  display: flex;
  gap: 16rpx;
  padding: 0 32rpx 24rpx;
}

.entry-item {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
  padding: 24rpx;
  background-color: #2a2a3e;
  border-radius: 16rpx;
  border: 1rpx solid #3a3a50;
}

.entry-icon {
  font-size: 28rpx;
}

.entry-text {
  font-size: 26rpx;
  color: #f5f5f5;
}

/* 区域标题 */
.section-header {
  padding: 16rpx 32rpx;
}

.section-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #f5f5f5;
}

/* 俱乐部列表 */
.club-list {
  padding: 0 32rpx;
  height: calc(100vh - 360rpx);
}

.club-card {
  display: flex;
  align-items: center;
  padding: 24rpx;
  background-color: #2a2a3e;
  border-radius: 20rpx;
  margin-bottom: 16rpx;
}

.club-avatar {
  width: 96rpx;
  height: 96rpx;
  background: linear-gradient(135deg, #32324a 0%, #1e1e32 100%);
  border-radius: 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20rpx;
  border: 1rpx solid #3a3a50;
}

.club-emoji {
  font-size: 44rpx;
}

.club-info {
  flex: 1;
}

.club-name-row {
  display: flex;
  align-items: center;
  gap: 12rpx;
  margin-bottom: 8rpx;
}

.club-name {
  font-size: 28rpx;
  font-weight: 600;
  color: #f5f5f5;
}

.club-level {
  background-color: rgba(246, 195, 66, 0.12);
  border-radius: 6rpx;
  padding: 2rpx 10rpx;
}

.level-text {
  font-size: 18rpx;
  color: #f6c342;
}

.club-meta {
  display: flex;
  gap: 16rpx;
  margin-bottom: 6rpx;
}

.meta-members,
.meta-region {
  font-size: 22rpx;
  color: #6b6b80;
}

.club-stats {
  display: flex;
  gap: 16rpx;
}

.stat-item {
  font-size: 20rpx;
  color: #b0b0c0;
}

.join-btn {
  border: 1rpx solid rgba(246, 195, 66, 0.5);
  border-radius: 12rpx;
  padding: 12rpx 20rpx;
  flex-shrink: 0;
}

.join-text {
  font-size: 22rpx;
  color: #f6c342;
  white-space: nowrap;
}
</style>
