<template>
  <view class="page">
    <!-- 顶部Tab -->
    <view class="ranking-tabs">
      <view class="rank-tab" :class="{ active: activeTab === 'personal' }" @tap="activeTab = 'personal'">
        <text class="rank-tab-text" :class="{ active: activeTab === 'personal' }">个人榜</text>
      </view>
      <view class="rank-tab" :class="{ active: activeTab === 'club' }" @tap="activeTab = 'club'">
        <text class="rank-tab-text" :class="{ active: activeTab === 'club' }">俱乐部榜</text>
      </view>
    </view>

    <!-- 分类筛选 -->
    <view class="filter-tabs">
      <view
        class="filter-tab"
        :class="{ active: activeFilter === f.value }"
        v-for="f in filters"
        :key="f.value"
        @tap="activeFilter = f.value"
      >
        <text class="filter-tab-text" :class="{ active: activeFilter === f.value }">{{ f.label }}</text>
      </view>
    </view>

    <!-- Top 3 -->
    <view class="podium-section">
      <!-- 第二名 -->
      <view class="podium-item">
        <view class="podium-avatar">
          <image src="/static/demo/avatar2.jpg" class="podium-img" mode="aspectFill" />
        </view>
        <text class="podium-name">李小编</text>
        <text class="podium-score">2650</text>
        <view class="podium-badge silver">
          <text class="badge-num">2</text>
        </view>
      </view>
      <!-- 第一名 -->
      <view class="podium-item first">
        <view class="crown-icon">👑</view>
        <view class="podium-avatar gold-ring">
          <image src="/static/demo/avatar1.jpg" class="podium-img" mode="aspectFill" />
        </view>
        <text class="podium-name">王大佬</text>
        <text class="podium-score highlight">3400</text>
        <view class="podium-badge gold">
          <text class="badge-num">1</text>
        </view>
      </view>
      <!-- 第三名 -->
      <view class="podium-item">
        <view class="podium-avatar">
          <image src="/static/demo/avatar3.jpg" class="podium-img" mode="aspectFill" />
        </view>
        <text class="podium-name">李掌门</text>
        <text class="podium-score">2480</text>
        <view class="podium-badge bronze">
          <text class="badge-num">3</text>
        </view>
      </view>
    </view>

    <!-- 排名列表 -->
    <scroll-view scroll-y class="ranking-scroll">
      <view class="ranking-item" v-for="item in rankingList" :key="item.rank">
        <text class="item-rank">{{ item.rank }}</text>
        <view class="item-avatar-wrap">
          <view class="item-avatar">
            <text class="avatar-char">{{ item.name.charAt(0) }}</text>
          </view>
        </view>
        <text class="item-name">{{ item.name }}</text>
        <text class="item-score">{{ item.score }}</text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const activeTab = ref('personal')
const activeFilter = ref('all')

const filters = [
  { label: '全部', value: 'all' },
  { label: '初级', value: 'beginner' },
  { label: '中级', value: 'mid' },
  { label: '高级', value: 'senior' },
]

const rankingList = ref([
  { rank: 4, name: '掼蛋小王子', score: 2200 },
  { rank: 5, name: '一把好牌', score: 2150 },
  { rank: 6, name: '快乐掼蛋', score: 2100 },
  { rank: 7, name: '天天向上', score: 2050 },
  { rank: 8, name: '陈总', score: 2000 },
  { rank: 9, name: '赵高手', score: 1950 },
  { rank: 10, name: '周教练', score: 1900 },
])
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #F5F5F5;
}

/* 排名Tab */
.ranking-tabs {
  display: flex;
  background-color: #FFFFFF;
  padding: 16rpx 24rpx;
  gap: 16rpx;
}

.rank-tab {
  padding: 12rpx 32rpx;
  border-radius: 32rpx;
  background-color: #F5F5F5;
}

.rank-tab.active {
  background-color: #C41E3A;
}

.rank-tab-text {
  font-size: 28rpx;
  color: #666666;
}

.rank-tab-text.active {
  color: #FFFFFF;
  font-weight: 600;
}

/* 筛选 */
.filter-tabs {
  display: flex;
  background-color: #FFFFFF;
  padding: 8rpx 24rpx 16rpx;
  gap: 24rpx;
  border-bottom: 1rpx solid #F0F0F0;
}

.filter-tab {
  padding: 8rpx 0;
}

.filter-tab.active {
  border-bottom: 4rpx solid #C41E3A;
}

.filter-tab-text {
  font-size: 26rpx;
  color: #999999;
}

.filter-tab-text.active {
  color: #C41E3A;
  font-weight: 500;
}

/* 领奖台 */
.podium-section {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding: 48rpx 32rpx 32rpx;
  background-color: #FFFFFF;
  gap: 32rpx;
  margin-bottom: 16rpx;
}

.podium-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
}

.podium-item.first {
  margin-bottom: 16rpx;
}

.crown-icon {
  font-size: 40rpx;
  margin-bottom: 4rpx;
}

.podium-avatar {
  width: 96rpx;
  height: 96rpx;
  border-radius: 50%;
  overflow: hidden;
  background-color: #F0F0F0;
}

.podium-avatar.gold-ring {
  width: 112rpx;
  height: 112rpx;
  border: 4rpx solid #FFD700;
}

.podium-img {
  width: 100%;
  height: 100%;
}

.podium-name {
  font-size: 26rpx;
  color: #333333;
  font-weight: 500;
}

.podium-score {
  font-size: 24rpx;
  color: #999999;
}

.podium-score.highlight {
  color: #C41E3A;
  font-weight: 700;
  font-size: 28rpx;
}

.podium-badge {
  width: 40rpx;
  height: 40rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.podium-badge.gold {
  background-color: #FFD700;
}

.podium-badge.silver {
  background-color: #C0C0C0;
}

.podium-badge.bronze {
  background-color: #CD7F32;
}

.badge-num {
  font-size: 22rpx;
  color: #FFFFFF;
  font-weight: 700;
}

/* 排名列表 */
.ranking-scroll {
  height: calc(100vh - 500rpx);
  padding: 0 24rpx;
}

.ranking-item {
  display: flex;
  align-items: center;
  padding: 20rpx 16rpx;
  background-color: #FFFFFF;
  border-radius: 12rpx;
  margin-bottom: 8rpx;
}

.item-rank {
  width: 60rpx;
  font-size: 28rpx;
  font-weight: 600;
  color: #999999;
  text-align: center;
}

.item-avatar-wrap {
  margin-right: 16rpx;
}

.item-avatar {
  width: 64rpx;
  height: 64rpx;
  border-radius: 50%;
  background-color: #FFF0F0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-char {
  font-size: 26rpx;
  color: #C41E3A;
  font-weight: 600;
}

.item-name {
  flex: 1;
  font-size: 28rpx;
  color: #333333;
}

.item-score {
  font-size: 28rpx;
  font-weight: 600;
  color: #C41E3A;
}
</style>
